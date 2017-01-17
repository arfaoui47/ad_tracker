from boto.s3.connection import S3Connection
from boto.s3.key import Key
from rootkey import *
import os.path
import sys


conn = S3Connection(AWSAccessKeyId, AWSSecretKey)
bucket = conn.get_bucket('adtracker-backet')


def upload_to_S3(md5_hash, file):
    
    k = Key(bucket)
    k.key = md5_hash
    k.set_contents_from_filename(file)
    k.make_public()
    os.remove(file)    	 			# remove file after checkusm
    print '[+] Deleting file ', file
    url = k.generate_url(expires_in=0, query_auth=False)
    return url


def upload_dir_to_S3(dir_name)
    sourceDir = dirname
    destDir = dirname


    uploadFileNames = []
    for (sourceDir, dirname, filename) in os.walk(sourceDir):
        uploadFileNames.extend(filename)
        break


def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

    for filename in uploadFileNames:
        sourcepath = os.path.join(sourceDir + filename)
        destpath = os.path.join(destDir, filename)
        print 'Uploading %s to Amazon S3 bucket %s' % \
               (sourcepath, bucket_name)

        filesize = os.path.getsize(sourcepath)
        if filesize > MAX_SIZE:
            print "multipart upload"
            mp = bucket.initiate_multipart_upload(destpath)
            fp = open(sourcepath,'rb')
            fp_num = 0
            while (fp.tell() < filesize):
                fp_num += 1
                print "uploading part %i" %fp_num
                mp.upload_part_from_file(fp, fp_num, cb=percent_cb, num_cb=10, size=PART_SIZE)

            mp.complete_upload()

        else:
            print "singlepart upload"
            k = Key(bucket)
            k.key = destpath
            k.set_contents_from_filename(sourcepath,
                    cb=percent_cb, num_cb=10)
