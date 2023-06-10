import chromadb
from flask import Flask, Blueprint
from flask_socketio import SocketIO, join_room, emit

from envapi import validation, database, handlers

print('\nFlask Establishing')
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable cross-origin resource sharing (CORS)

# Initialize ChromaDB 
client = chromadb.Client()

# ChromaDB collections
objects_collection = client.get_or_create_collection("objects")
agents_collection = client.get_or_create_collection("agents") 
events_collection = client.get_or_create_collection("events")
locations_collection = client.get_or_create_collection("locations")

handlers.init_handlers(socketio, objects_collection, agents_collection, events_collection)
print('\nHandlers Initted')

# REST API endpoint to get details of all objects
@app.route('/objects')
def get_objects():
    objects = database.objects_collection.get_all()
    print(f'\nObjects endpoint: {objects}')
    return jsonify(objects)

# REST API endpoint to get details of a single object by ID
@app.route('/objects/<object_id>')    
def get_object(object_id):
    object = database.objects_collection.get(object_id)
    print(f'\nSpecific Object endpoint: {object}')
    return jsonify(object)

#Room endpoints
@app.route('/stream/<room_id>')
def stream(room_id):
    def generate():
        while True:
            # Retrieve or generate your event data here
            event_data = get_event_data(room_id)
            if event_data is not None:
                yield f"data:{event_data}\n\n"
    print(f'\nEvent Data: {event_data}')
    return app.response_class(generate(), mimetype='text/event-stream')

@socketio.on('join', namespace='/stream')  
def on_join(data):  
    username = data['username']
    room = data['room']
    join_room(room)  
    
@socketio.on('speak', namespace='/stream')
def speak(data):  
    message = data['message']
    room = data['room']
    emit('spoken_message', {'message': message}, room=room)       

@app.route('/speak/', methods=['POST'])
def speak_message():
    data = request.get_json()
    room_id = data['room'] 
    message = data['message']
    emit('spoken_message', {'message': message}, namespace=f'/stream/{room_id}') 

@app.route('/send/<receiver_id>', methods=['POST'])
def send_message(receiver_id):
    data = request.get_json()
    message = data['message']
    emit('direct_message', {'message': message}, namespace=f'/{receiver_id}')
    print(f'\nEvent Data: {message}')
    return 'Message sent!'

# Endpoint for agents to request creation of a new object 
@app.route('/objects', methods=['POST'])
def create_object():
    # Get required details from request
    data = request.get_json()
    # Validate request payload
    valid, errors = validation.validate_create(data)
    if not valid:
        return jsonify({
            "errors": errors
        }), 400
    print(f'\nError Creating Object: {data}')
    # Create new object
    object = {
        'name': data['name'],
        'description': data['description'],
        'required': data['required'] 
    }
    # Add object to ChromaDB collection
    database.objects_collection.add(object)
    print(f'\nCreate Object: {object}')
    return jsonify(object), 201     

locations_blueprint = Blueprint('locations', __name__)

@locations_blueprint.route('/locations', methods=['POST'])
def create_location():
    is_valid, error = validation.validate_location(request)
    if not is_valid:
        return jsonify({"error": error}), 400
        print(f'Error Creating Location: {request}')
    try:
        new_location = {
            'name': request.json['name'],
            'coordinates': {
                'x': request.json['coordinates']['x'],
                'y': request.json['coordinates']['y']  
            }
        }
        location_id = database.locations_collection.add(new_location)
        print(f'\nCreate Location: {new_location}')
        return jsonify(new_location), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.register_blueprint(locations_blueprint)

if __name__ == '__main__': 
    print('Run Socket')
    socketio.run(app)
    print('Socket Running')
