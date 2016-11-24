from boto.s3.connection import S3Connection
from boto.s3.key import Key
from rootkey import *
import os


def upload_to_S3(md5_hash, file):
    conn = S3Connection(AWSAccessKeyId, AWSSecretKey)
    bucket = conn.get_bucket('adtracker-backet')
    k = Key(bucket)
    k.key = md5_hash
    k.set_contents_from_filename(file)
    k.make_public()
    # os.remove(file)    	 								#TODO #remove file after checkusm
    print '[+] Deleting file ', file
