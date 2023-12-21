import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    target_bucket = 'uwf-poc-bucket'

    try:
        detail = event['detail'] if isinstance(event['detail'], dict) else json.loads(event['detail'])
        source_bucket = detail['bucket']
        processed_file_key = detail['key']
        download_path = f'/tmp/{processed_file_key.split("/")[-1]}'

        # Download the processed file from S3
        s3.download_file(source_bucket, processed_file_key, download_path)

        # Upload the file to the target bucket
        final_file_key = f'{processed_file_key}-final'
        s3.upload_file(download_path, target_bucket, final_file_key)

        logger.info(f'Processed file uploaded to target bucket: {final_file_key}')
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Processed file uploaded to target bucket'})
        }
    except Exception as e:
        logger.error(f'Error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
