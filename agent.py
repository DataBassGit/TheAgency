import logging
import requests
import chromadb
from datetime import datetime

from objectives import get_current_objective

logging.basicConfig(level=logging.INFO)

class Agent:
    def __init__(self, agent_id, summary_description, environment_url):
        self.agent_id = agent_id
        self.summary_description = summary_description
        self.environment_url = environment_url
        self.logger = logging.getLogger(__name__)
        
        # Connect to ChromaDB
        self.client = chromadb.Client()  
    
        # Create a collection for this agent's memory
        self.memory = self.client.get_or_create_collection(f"agent_{self.agent_id}")  
    
        # Create index on memory collection
        if self.memory.count() > 0:
            self.memory.create_index()

    def generate_action(self):
        objective = get_current_objective(self.agent_id)
        room_objects = requests.get(f"{self.environment_url}/room_objects").json()
        previous_action = self.get_previous_action()
        event = self.get_current_event() or "none"
        
        # Construct query to retrieve relevant memories based on context
        query = {
            "where": {
                "objective": objective,
                "room_objects": {
                    "$in": room_objects 
                },
                "previous_action": previous_action,
                "event": event 
            }
        }
        
        # Query memory and add any results to summary as context
        relevant_memories = self.memory.query(query)
        context = "\n\nContext: "
        for memory in relevant_memories:
            context += f"{memory['objective']}, "
            context += f"{', '.join(memory['room_objects'])}, "
            context += f"{memory['previous_action']}, " 
            context += f"{memory['event']}, "
        self.summary_description += context  
        
        # Generate next action based on summary and memories
        action = self._generate_action(self.summary_description, relevant_memories, self.environment_url)
        self.logger.info(f"Action: {action}")
        return action 

    def _generate_action(self, summary, memories, environment_url):
        # Example logic for generating an action - This will be dependent on your exact use case
        return "generated_action"
        
    def react(self, observation):
        reaction = requests.post(f"{self.environment_url}/react", json={
            "observation": observation,
            "agent_id": self.agent_id
        }).json()
        self.logger.info(f"Reaction: {reaction}")
        return reaction

    def add_event_to_memory(self, event, id):
        self.memory.add(  
            documents=[event], 
            metadatas={"agent_id": id(self), "timestamp": datetime.now().isoformat()},  
            ids=[id]  
        )  

    def analyze_memory(self):  
        memory_analysis = self.memory.analyze(metrics=["count"], group_by=["timestamp"])  
        self.logger.info(f"Memory analysis: {memory_analysis}")

    def get_previous_action(self):
        # Retrieve previous action from memory
        if self.memory.count() > 0:
            return self.memory.query({})[-1]["previous_action"]
        return None

    def get_current_event(self):
        # Example logic for getting current event - This will be dependent on your exact use case
        return "current_event"
