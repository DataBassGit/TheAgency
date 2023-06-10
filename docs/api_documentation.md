Here is a draft documentation for the environment API:

# Environment API Documentation

The environment provides an API for agents to interact with the system. This includes:

- A REST API for creating, reading, updating and deleting data
- A websocket API for real-time communication and event streaming

## REST API

The REST API allows agents to query the environment for data, create new data entries and update or delete existing entries.

### Endpoints

**/objects**

- GET: Retrieve details of all objects 
- POST: Create a new object

**/objects/\<object_id>**

- GET: Retrieve details of a single object by ID

**/locations**

- POST: Create a new location

**/react**

- POST: Record an agent's reaction to an event 

### Payloads

**POST /objects**

- Payload:

```json
{
  "name": "string", 
  "description": "string", 
  "required": ["string1", "string2"] 
}
```

- Response: The created object

Status Codes:

- 201 Created 
- 400 Bad Request (if invalid payload)

**POST /locations**

- Payload: 

```json
{
  "name": "string",
  "coordinates": {
    "x": integer,
    "y": integer
  }
}
```

- Response: The created location

Status Codes: 

- 201 Created
- 400 Bad Request (if invalid payload)
- 500 Internal Server Error

**POST /react**

- Payload:

```json
{
  "observation": "string",
  "agent_id": "string" 
}
```

- Response: The reaction to the event

### Error Handling

- 400 Bad Request: Returned if an invalid payload is sent 
- 500 Internal Server Error: Returned if there is an error creating a location

## Websocket API

The environment uses Flask-SocketIO to enable real-time communication over websockets. This includes:

- Event streaming: Agents can subscribe to environment events 
- Direct messaging: Agents can send direct messages to each other

### Events

**'object updated'** - Emitted when an object is updated

**'object deleted'** - Emitted when an object is deleted

**'event created'** - Emitted when a new event is created in the environment

**'spoken_message'** - Emitted when an agent sends a message in a room

### Namespaces

**/stream/\<room_id>** - For room messaging

**/\<agent_id>** - For direct messaging an agent

### Usage

Agents can connect to the websocket API at `ws://environment_url/stream`.

To join a room and receive messages:

```json
{ "join": {"username": "agent1", "room": "room1"}} 
```

To send a message to a room:

```json
{"speak": {"message": "Hello", "room": "room1"}}
```

To send a direct message to an agent:

```json
{"message": "Hello"}
``` 
(sent to the /<agent_id> namespace)

Let me know if you would like me to clarify or expand the documentation in any way. I hope this helps in developing the environment and agent APIs!