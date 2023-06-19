import boto3
import zipfile
import os
import tempfile

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    with tempfile.TemporaryDirectory() as tmpdir:
        download_path = os.path.join(tmpdir, os.path.basename(key))
        
        s3_client.download_file(bucket_name, key, download_path)
        
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        for file in os.listdir(tmpdir):
            if file != os.path.basename(key):  # Don't upload the original zip file
                s3_client.upload_file(os.path.join(tmpdir, file), bucket_name, file)
