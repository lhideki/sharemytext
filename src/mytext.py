import json
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def create_response(status_code = 200, body = None):
    res = {
        'statusCode': status_code,
        'body': body
    }
    
    return res

def get(event, context):
    id = event['pathParameters']['id']
    text = id
    
    data = {
        'output': text,
        'timestamp': datetime.datetime.utcnow().isoformat()
    }

    return create_response(body = json.dumps(data))

def post(event, context):
    id = event['pathParameters']['id']
    text = event['body']['text']
    now = datetime.datetime.now()
    data = {
        'id': id,
        'text': text,
        'lastUpdatedDate': now
    }
    
    logger.info(data)
    
    return create_response()