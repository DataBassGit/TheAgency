import json
import requests
import uuid

from agent import Agent

import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    # Generate a uuid for the agent ID
    agent_id = str(uuid.uuid4())

    environment_url = "http://localhost:5000"

    summary_description = "I am a test agent for the environment API."

    agent = Agent(agent_id, summary_description, environment_url)

    # Test POST /objects endpoint
    try:
        new_object = {
            "name": "Test Object",
            "description": "This is a test object",
            "required": ["item1", "item2"]
        }
        response = requests.post(f"{environment_url}/objects", json=new_object)
        print(f"Create object response: {response.json()}")
    except Exception as e:
        print(f"Error creating object: {e}")

    # Test GET /objects/<object_id> endpoint
    try:
        object_id = response.json()["_id"]
        obj = requests.get(f"{environment_url}/objects/{object_id}").json()
        print(f"Object {object_id}: {obj}")
    except Exception as e:
        print(f"Error getting object: {e}")



    # Test POST /locations endpoint
    try:
        new_location = {
            "name": "Test Location",
            "coordinates": {
                "x": 10,
                "y": 20
            }
        }
        response = requests.post(f"{environment_url}/locations", json=new_location)
        print(f"Create location response: {response.json()}")
    except Exception as e:
        print(f"Error creating location: {e}")



    # Test POST /react endpoint
    try:
        reaction_data = requests.post(f"{environment_url}/react", json={
            "observation": "Test event",
            "agent_id": agent_id
        }).json()
        print(f"Reaction: {reaction_data}")
    except Exception as e:
        print(f"Error posting reaction: {e}")

    # Test joining a room
    try:
        agent.join_room("test_room")
        print("Joined room")
    except Exception as e:
        print(f"Error joining room: {e}")

    # Test sending a message to a room
    try:
        message = {"speak": {"message": "Hello from test agent!", "room": "test_room"}}
        agent.websocket.send(json.dumps(message))
        print("Message sent to room")
    except Exception as e:
        print(f"Error sending message to room: {e}")

    # Test sending a direct message to another agent
    try:
        receiver_id = "another_agent_id"  # Replace this with the actual agent ID
        message = {"message": "Direct message from test agent"}
        agent.websocket.send(json.dumps(message))
        print(f"Direct message sent to {receiver_id}")
    except Exception as e:
        print(f"Error sending direct message: {e}")

    # Test GET /objects endpoint
    try:
        response = requests.get(f"{environment_url}/objects")
        print(f"GET /objects status code: {response.status_code}")
        print(f"GET /objects response content: {response.content}")
        objects = response.json()
        print(f"Objects: {objects}")
    except Exception as e:
        print(f"Error getting objects: {e}")
