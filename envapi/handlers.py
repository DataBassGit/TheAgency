from .database import objects_collection, agents_collection, events_collection

@socketio.on('update object')  
def handle_object_update(data):
    object = objects_collection.get(data['id'])
    object['state'] = data['new_state']
    objects_collection.update({'id': data['id']}, object)
    socketio.emit('object updated', object)

@socketio.on('delete object')
def handle_object_delete(data):
    objects_collection.delete(data['id'])
    socketio.emit('object deleted', data)

@socketio.on('create event')
def handle_event_creation(data):
    event = {
        'type': data['type'],
        'payload': data['payload'],
        'timestamp': datetime.utcnow()
    }
    event_id = events_collection.add(event)
    socketio.emit('event created', event) 