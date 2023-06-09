from agent import Agent
import logging

logging.basicConfig(level=logging.INFO)

class Agent:
    # Existing Agent code...

    def react(self, observation): 
        reaction = requests.post(f"{self.environment_url}/react", json={
            "observation": observation,
            "agent_id": self.agent_id
        }).json()
        return reaction 

if __name__ == "__main__":
    agent_id_1 = "1"  
    agent_id_2 = "2"
    environment_url = "http://localhost:5000"  

    summary_description_1 = "I am a university student studying computer science..."   
    summary_description_2 = "I am another student at the university."

    agent_1 = Agent(agent_id_1, summary_description_1, environment_url)
    agent_2 = Agent(agent_id_2, summary_description_2, environment_url)

    # Generate initial action
    action_1 = agent_1.generate_action()
    logging.info(f"Action of Agent 1: {action_1}")

    # Generate a reaction introducing the other agent 
    observation = f"You see your friend {agent_2.summary_description}"
    reaction_1 = agent_1.react(observation)
    logging.info(f"Reaction of Agent 1: {reaction_1}")

    # Continue dialogue between agents
    dialogue = [
        agent_1.generate_action(),
        agent_2.react(agent_1.memory.last()), 
        agent_1.react(agent_2.memory.last())
    ]

    # Log the dialogue  
    for line in dialogue:
        logging.info(f"Dialogue: {line}")
