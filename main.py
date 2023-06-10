import uuid
from agent import Agent 
import logging 

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # Generate a uuid for the agent ID
    agent_id = str(uuid.uuid4())
    room_id = "123" 
    environment_url = "http://localhost:5000"

    summary_description = "I am a university student studying computer science..."

    agent = Agent(agent_id, summary_description, environment_url)

    agent.name = "Agent 1"
    agent.join_room(room_id)
    
    try: 
        agent.socketIO.wait()
    except Exception as e:
        logging.error(f"Error in agent {agent.name}: {e}")
    finally:
        # Gracefully close the agent 
        logging.info(f"Closing agent {agent.name}")
