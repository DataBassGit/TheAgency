import logging
import json
import requests
import chromadb
from datetime import datetime
import websockets
import asyncio
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

        # Create an events collection to store events
        self.events = self.client.get_or_create_collection("events")

        # Create index on memory collection
        if self.memory.count() > 0:
            self.memory.create_index()

    async def join_room(self, room_id):
        uri = f"ws://{self.environment_url}/stream"
        print(f'\nDestination URL: {uri}')
        async with websockets.connect(uri) as websocket:
            try:
                self.websocket = websocket
            except Exception as e:
                print(f'\n Exception when connection websocket: {e}')
            await websocket.send(json.dumps({"join": {"username": self.agent_id, "room": room_id}}))
            print('Room Joined')

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()

    async def get_current_event(self):
        # Query for all events in the events collection
        current_events = self.events.query({})
        
        # If there are no events, return None
        if len(current_events) == 0:
            return None
        
        # Get event descriptions from the events
        event_descriptions = [event['document'] for event in current_events]
        
        # Delete all events in the collection after retrieval
        event_ids = [event['_id'] for event in current_events]
        for event_id in event_ids:
            self.events.delete(event_id)  
            
        # Return the event descriptions
        return event_descriptions

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

async def async_main():
    try: 
        print('\nJoining room')
        await agent.join_room("sample_room")
    except Exception as e:
        logging.error(f"Error in agent {agent.agent_id}: {e}")
    finally:
        # Gracefully close the agent
        print('\nleaving Room')
        await agent.disconnect()
        logging.info(f"Closing agent {agent.agent_id}")

if __name__ == '__main__':
    agent_id = "sample_agent"
    summary_description = "This is a sample agent."
    environment_url = "localhost:5000"
    agent = Agent(agent_id, summary_description, environment_url)
    asyncio.run(async_main())

