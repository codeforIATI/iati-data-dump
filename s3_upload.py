"""Upload a file to S3."""

import argparse
from os.path import basename, exists, isfile
import sys
import boto3


parser = argparse.ArgumentParser(description='Upload a file to s3')
parser.add_argument('filename',
                    help='Local file to upload')
parser.add_argument('bucket',
                    help='Bucket name in S3')


def main():
    args = parser.parse_args()

    bucket = args.bucket
    filename = args.filename
    if not exists(filename):
        print(filename, 'does not exist on your filesystem')
        sys.exit(1)
    elif not isfile(filename):
        print(filename, 'is not a folder on your filesystem')
        sys.exit(1)

    upload(filename, bucket)


def upload(filename, bucket, object_name=None):
    """Upload a file to an S3 bucket"""

    # If S3 object_name was not specified, use filename
    if object_name is None:
        object_name = basename(filename)

    # Upload the file
    s3_client = boto3.client("s3")
    s3_client.upload_file(
        filename, bucket, object_name,
        ExtraArgs={'ACL': 'public-read'})


if __name__ == '__main__':
    main()
