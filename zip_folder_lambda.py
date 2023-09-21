import boto3
import os
import zipfile

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Specify the S3 bucket and folder you want to zip
    source_bucket = 'your-source-bucket'
    source_folder = 'your-source-folder'
    target_bucket = 'your-target-bucket'
    target_key = 'your-target-folder/your-folder.zip'

    # Create a temporary directory
    temp_dir = '/tmp'
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Download the contents of the S3 folder to the temporary directory
        s3.download_file(source_bucket, source_folder, f'{temp_dir}/folder_contents.zip')

        # Create a zip file with the contents
        with zipfile.ZipFile(f'{temp_dir}/your-folder.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

        # Upload the zip file to the target S3 location
        s3.upload_file(f'{temp_dir}/your-folder.zip', target_bucket, target_key)

        return {
            'statusCode': 200,
            'body': 'Folder zipped and uploaded successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
    finally:
        # Clean up: Remove temporary files
        os.remove(f'{temp_dir}/your-folder.zip')
        os.remove(f'{temp_dir}/folder_contents.zip')
