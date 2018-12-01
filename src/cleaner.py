from datetime import datetime, timedelta
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
texts_table = dynamodb.Table('sharemytext.Texts')

def create_response(status_code = 200, body = None):
    res = {
        'statusCode': status_code,
        'body': 'OK'
    }
    
    return res

def clean(event, context):
    now = datetime.utcnow()
    target_date = now - timedelta(hours=1)
    
    logger.info(f'Cleanaing less than {target_date.isoformat()}/{datetime.utcnow().isoformat()}.')
    
    filter = Key('lastUpdatedDate').lt(target_date.isoformat())
    res = texts_table.scan(
        FilterExpression = filter
    )
    if 'Items' not in res:
        return create_response(body = 'NOP')
    
    for item in res['Items']:
        id = item['id']
        
        logger.info(f'Deleting id:{id}.')
        
        res = texts_table.delete_item(
            Key = {
                'id': id
            }
        )
        logger.info(res)
    logger.info('Clean up completed.')
    
    return create_response()