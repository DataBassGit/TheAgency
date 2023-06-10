# Remove this line: from .database import objects_collection, agents_collection, events_collection

# No decorators here - we'll add those in the init_handlers function
def handle_object_update(data):
    object = objects_collection.get(data['id'])
    object['state'] = data['new_state']
    objects_collection.update({'id': data['id']}, object)
    socketio.emit('object updated', object)

def handle_object_delete(data):
    objects_collection.delete(data['id'])
    socketio.emit('object deleted', data)

def handle_event_creation(data):
    event = {
        'type': data['type'],
        'payload': data['payload'],
        'timestamp': datetime.utcnow()
    }
    event_id = events_collection.add(event)
    socketio.emit('event created', event)

# Add this function to initialize your handlers
def init_handlers(socketio, objects_collection, agents_collection, events_collection):
    @socketio.on('update object')  
    def on_object_update(data):
        handle_object_update(data)

    @socketio.on('delete object')
    def on_object_delete(data):
        handle_object_delete(data)

    @socketio.on('create event')
    def on_event_creation(data):
        handle_event_creation(data)
