import chromadb
from flask import Flask, Blueprint
from flask_socketio import SocketIO

from envapi import validation, database, handlers

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize ChromaDB 
client = chromadb.Client()

# ChromaDB collections
objects_collection = client.get_or_create_collection("objects")
agents_collection = client.get_or_create_collection("agents") 
events_collection = client.get_or_create_collection("events")
locations_collection = client.get_or_create_collection("locations")

handlers.init_handlers(socketio, objects_collection, agents_collection, events_collection)

# ... rest of your code ...


# REST API endpoint to get details of all objects
@app.route('/objects')
def get_objects():
    objects = database.objects_collection.get_all()
    return jsonify(objects)

# REST API endpoint to get details of a single object by ID
@app.route('/objects/<object_id>')    
def get_object(object_id):
    object = database.objects_collection.get(object_id)
    return jsonify(object)

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
    # Create new object
    object = {
        'name': data['name'],
        'description': data['description'],
        'required': data['required'] 
    }
    # Add object to ChromaDB collection
    database.objects_collection.add(object)
    return jsonify(object), 201     

locations_blueprint = Blueprint('locations', __name__)

@locations_blueprint.route('/locations', methods=['POST'])
def create_location():
    is_valid, error = validation.validate_location(request)
    if not is_valid:
        return jsonify({"error": error}), 400
    try:
        new_location = {
            'name': request.json['name'],
            'coordinates': {
                'x': request.json['coordinates']['x'],
                'y': request.json['coordinates']['y']  
            }
        }
        location_id = database.locations_collection.add(new_location)
        return jsonify(new_location), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.register_blueprint(locations_blueprint)

if __name__ == '__main__': 
    socketio.run(app)
