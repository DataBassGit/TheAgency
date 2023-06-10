
# Collaborative Multi-Agent Environment 

This project aims to develop an environment that supports collaboration and problem-solving between intelligent software agents. The environment provides agents with a platform to interact, exchange information, coordinate actions, and work together towards complex objectives. You can read the full exchange here: https://chat.openai.com/share/7f4e6b21-7c6e-4efe-9a97-615831b3c059 

## Key Features

- Flask REST API and event streaming for agent interaction 
- Scalable database (ChromaDB) for data storage
- Lifecycle and validation models to ensure data integrity  
- Supports connecting local or remote agents to the environment
- Enables agents to react dynamically based on environment events  
- Decoupled from specific agent architectures - can support diverse agent models  

## Getting Started


### Installation

1. Clone the repo:
```bash
git clone https://github.com/DataBassGit/GenerativeAgent.git
```

2. Install dependencies:  
```bash
pip install -r requirements.txt
```

3. Run the environment server:
```bash
python environment.py 
```

4. Start agent services to connect to the local or remote environment 

## Key Libraries

- Flask, Flask-SocketIO: used to build and handle the REST API and event streaming.
- Cerberus: provides data validation.
- ChromaDB: offers scalable database solutions for storing data.
- Requests: helps with making HTTP requests to the API.


## Roadmap

- Continue enhancing environment functionality based on testing and feedback
- Build tools and platforms to streamline development of agents for the environment  
- Explore options for scaling the environment to support more sophisticated agent interaction and swarm-level behavior 
- Investigate privacy-preserving and fair information exchange between agents 
- Release stable versions of the environment for community access and development

