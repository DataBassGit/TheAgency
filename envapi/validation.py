from cerberus import Validator

def validate_location(request):
    schema = {
        'name': {'type': 'string'},
        'coordinates': {
            'type': 'dict',
            'schema': {
                'x': {'type': 'integer'},
                'y': {'type': 'integer'}
            }
        }
    }
    v = Validator(schema)
    if v.validate(request.json, schema):
        return True, None
    else:
        return False, v.errors

def validate_create(data):
    create_schema = {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'required': {'type': 'list', 'schema': {'type': 'string'}}
    }
    v = Validator(create_schema)
    if v.validate(data, create_schema):
        return True, None
    else:
        return False, v.errors  