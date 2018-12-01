import json
import datetime
import logging

def create_response(status_code = 200, body = None):
    res = {
        'statusCode': status_code,
        'body': body
    }
    
    return res

def get(event, context):
    id = event.id
    text = id
    
    data = {
        'output': text,
        'timestamp': datetime.datetime.utcnow().isoformat()
    }

    return create_response(body = json.dumps(data))

def post(event, context):
    id = event.id
    text = event.text
    now = datetime.datetime.now()
    data = {
        'id': id,
        'text': text,
        'lastUpdatedDate': now
    }
    
    logging.info(data)
    
    return create_response()