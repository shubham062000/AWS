import logging
import boto3
from botocore.exceptions import ClientError
import os
import glob

client = boto3.client('s3')

def upload_file(file_name, bucket, object_name=None):
    ''' Function for uploading files to AWS s3 '''
    
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# upload single File
upload_file('File Location','BucketName')


# upload multiple Files
files = glob.glob('FilesLocation/*') # give /* after directory to include all files

for file in files:
    try:
        upload_file(file,'BucketName')
        print('uploaded :', file)
    except IsADirectoryError as e:  # For ignoring IsADirectoryError
        logging.error(e)
        
# To get all buckets name presented in s3
s3 = boto3.resource('s3')

for buckets in s3.buckets.all():
    print(buckets.name)
    
bucket = s3.Bucket('BucketName')
files = list(bucket.objects.all())


# Download all files presented in bucket
for file in files:
    client.download_file('BucketName',file.key,file.key)
    print('downloaded :', file)