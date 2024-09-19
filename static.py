import boto3
import json
from botocore.exceptions import ClientError

# Initialize the S3 client
region = 'us-east-1'  # Change this to the region where you want to create the bucket
s3_client = boto3.client('s3', region_name=region)

def setup_bucket(bucket_name, object_key, file_path):
    def bucket_exists(bucket_name):
        """Check if the bucket exists."""
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return bucket_name in buckets

    def delete_bucket(bucket_name):
        """Delete all objects in the bucket and then delete the bucket itself."""
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
        s3_client.delete_bucket(Bucket=bucket_name)

    try:
        # Check if bucket exists, delete and recreate if necessary
        if bucket_exists(bucket_name):
            print(f'Bucket {bucket_name} already exists. Deleting and recreating...')
            delete_bucket(bucket_name)
            print(f'Bucket {bucket_name} deleted successfully.')

        # Create a new bucket
        if region == 'us-east-1':
            response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            response = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f'Bucket {bucket_name} created successfully')

        # Set bucket access policies
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        print(f'Public access block settings disabled for {bucket_name}')

        # Set bucket policy for public read access
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(bucket_policy)
        )
        print(f'Bucket policy set to allow public read access for {bucket_name}')

        # Enable static website hosting
        website_configuration = {
            'IndexDocument': {'Suffix': 'index.html'},
            'ErrorDocument': {'Key': 'error.html'}  # Optional: error document
        }
        s3_client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration=website_configuration
        )
        print(f'Static website hosting enabled for {bucket_name}')

        # Upload the file to the bucket
        try:
            s3_client.upload_file(
                file_path, bucket_name, object_key,
                ExtraArgs={'ContentType': 'text/html'}
            )
            print('File uploaded successfully with ContentType set to text/html')
        except ClientError as upload_error:
            print(f'File upload error: {upload_error}')

        # Provide website URL
        website_url = f'http://{bucket_name}.s3-website-{region}.amazonaws.com/{object_key}'
        print(f'Your website is available at: {website_url}')

    except ClientError as e:
        print(f'Error: {e}')
