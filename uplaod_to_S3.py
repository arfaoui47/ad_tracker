from boto.s3.connection import S3Connection
from boto.s3.key import Key
from rootkey import *

conn = S3Connection(AWSAccessKeyId, AWSSecretKey)
bucket = conn.get_bucket('adtracker-backet')
k = Key(bucket)
k.key = 'html' # for example, 'images/bob/resized_image1.png'
k.set_contents_from_filename('main.py')