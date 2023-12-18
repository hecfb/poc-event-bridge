import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'uwf-poc-bucket'

    logger.info(f"Received event: {event}")

    try:

        message = json.loads(event['detail'])['message']
        formatted_message = message.title()  

        logger.info(f"Formatted message: {formatted_message}")

        file_name = 'message.txt'
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=formatted_message)

        logger.info(f"Message saved to S3 bucket: {bucket_name}")

    except Exception as e:
        logger.error(f"Error processing event: {e}")
        raise e

    return {'status': 'Message saved to S3'}
