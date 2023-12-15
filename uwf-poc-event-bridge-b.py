import boto3
import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'uwf-poc-bucket'

    # Log the received event
    logger.info(f"Received event: {event}")

    try:
        # Process the message
        message = json.loads(event['detail'])['message']
        formatted_message = message.title()  # Convert to "Hello World"

        # Log the formatted message
        logger.info(f"Formatted message: {formatted_message}")

        # Save the formatted message to S3
        file_name = 'message.txt'
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=formatted_message)

        logger.info(f"Message saved to S3 bucket: {bucket_name}")

    except Exception as e:
        logger.error(f"Error processing event: {e}")
        raise e

    return {'status': 'Message saved to S3'}
