import boto3
import os
import zipfile

s3 = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = 'your-source-bucket'
    source_folder = 'your-source-folder'
    target_bucket = 'your-target-bucket'
    target_key = 'your-target-folder/file_name.zip'
    
    temp_dir = '/tmp'
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # List objects in the source folder
        objects = s3.list_objects_v2(Bucket=source_bucket, Prefix=source_folder)
        
        # Create a new zip file to store the contents
        zip_filepath = os.path.join(temp_dir, 'your-folder.zip')
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for obj in objects.get('Contents', []):
                obj_key = obj['Key']
                local_path = os.path.join(temp_dir, os.path.basename(obj_key))
                
                # Download the S3 object to local temp directory
                s3.download_file(source_bucket, obj_key, local_path)
                
                # Add the downloaded file to the zip
                zipf.write(local_path, os.path.basename(local_path))
                
                # Optionally, remove the downloaded file from local directory to save space
                os.remove(local_path)
                
        # Upload the zip file to the target S3 location
        s3.upload_file(zip_filepath, target_bucket, target_key)

        return {
            'statusCode': 200,
            'body': 'Folder zipped and uploaded successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
