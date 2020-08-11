# settings for Amazon S3:
import os

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'social-network-drf'
AWS_S3_REGION_NAME = "ap-northeast-2"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

# Django Storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

