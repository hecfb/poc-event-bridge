import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    eventbridge = boto3.client('events')
    event_detail = {
        'source': 'lambda.a',
        'detail-type': 'message',
        'detail': json.dumps({'message': 'hELLO wORLD'})
    }

    try:
        response = eventbridge.put_events(
            Entries=[
                {
                    'Source': event_detail['source'],
                    'DetailType': event_detail['detail-type'],
                    'Detail': event_detail['detail'],
                },
            ]
        )
        logger.info(f"EventBridge response: {response}")
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Event sent successfully'})
        }

    except Exception as e:
        logger.error(f"Error publishing to EventBridge: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
