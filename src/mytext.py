import json
import datetime
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
texts_table = dynamodb.Table('sharemytext.Texts')

def create_response(status_code = 200, body = None):
    res = {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': json.dumps(body)
    }
    
    return res

def get(event, context):
    id = event['pathParameters']['id']
    res = texts_table.get_item(
        Key = {
            "id": id
        }
    )

    if 'Item' in res:
        item = res['Item']
        data = {
            'isExists': True,
            'text': item['text'],
            'lastUpdatedDate': item['lastUpdatedDate']
        }
    else:
        data = {
            'isExists': False,
            'text': None,
            'timestamp': datetime.datetime.utcnow().isoformat()
        }

    return create_response(body = data)

def post(event, context):
    id = event['pathParameters']['id']
    body = json.loads(event['body'])
    text = body['text']
    now = datetime.datetime.now()
    data = {
        'id': id,
        'text': text,
        'lastUpdatedDate': now.isoformat()
    }
    
    logger.info(data)
    res = texts_table.put_item(
        Item = data
    )
    status_code = res['ResponseMetadata']['HTTPStatusCode']
    
    if status_code > 200:
        return create_response(status_code = status_code,
            body = {
                "status": "Creation error"
            })
    else:
        return create_response(body = {"status": "OK"})