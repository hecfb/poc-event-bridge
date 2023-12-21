import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    eventbridge = boto3.client('events')
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    download_path = f'/tmp/{file_key}'

    try:
        # Download and process the file
        s3.download_file(source_bucket, file_key, download_path)
        with open(download_path, 'r') as file:
            data = json.load(file)
            for item in data:
                item['isActive'] = not item['isActive']

        # Upload processed data to S3
        processed_file_key = f'processed/{file_key}'
        upload_path = f'/tmp/processed_{file_key}'
        with open(upload_path, 'w') as file:
            json.dump(data, file)
        s3.upload_file(upload_path, source_bucket, processed_file_key)

        # Publish an event to EventBridge with the S3 reference
        event_detail = {
            'source': 'uwf-poc-event-bridge-a',
            'detail-type': 'processedFile',
            'detail': json.dumps({'bucket': source_bucket, 'key': processed_file_key})
        }
        response = eventbridge.put_events(Entries=[{
            'Source': event_detail['source'],
            'DetailType': event_detail['detail-type'],
            'Detail': event_detail['detail']
        }])
        logger.info("Event sent to EventBridge: " + json.dumps(response))
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'File processed and event sent'})
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
