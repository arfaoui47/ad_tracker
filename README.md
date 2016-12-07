# ad_tracker
[![Build Status](https://travis-ci.com/arfaoui47/ad_tracker.svg?token=CH8XvMgBpfMsqsoWSUb5&branch=master)](https://travis-ci.com/arfaoui47/ad_tracker)
[![Code Climate](https://codeclimate.com/github/arfaoui47/ad_tracker/badges/gpa.svg)](https://codeclimate.com/github/arfaoui47/ad_tracker)

Requirements
============

* Python 2.7 
* Works on Linux, Windows, Mac OSX, BSD
* Firefox >~ 48.0 version
* MySQL >~ 5.0

Install
=======
Install Python requirements
```sh  
pip install -r requirements.txt
``` 
Install Tor and Privoxy
```sh
sudo apt-get install tor privoxy
```  
Reject Exit node mode. Modify file /etc/tor/torrc:
```sh
ExitPolicy reject *:* # no exits allowed
```
Set Privoxy to forward through Tor:
```sh
echo 'echo "forward-socks5 / localhost:9050 ." >> /etc/privoxy/config' | sudo -s
```
Create rootkey.py file with AWS Access Key ID and Secret Access Key:
```py
AWSAccessKeyId=""
AWSSecretKey=""
```
Update conf.ini file with MySQL details:
```sh
[MySQL]

host : localhost
user : 
password : 
db : 
```
Update S3-bucket name in file upload_to_S3.py:
```py
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from rootkey import *
import os

def upload_to_S3(md5_hash, file):
        conn = S3Connection(AWSAccessKeyId, AWSSecretKey)
        bucket = conn.get_bucket('bucket-name')                    # Bucket Name
        k = Key(bucket)
        k.key = md5_hash 
        k.set_contents_from_filename(file)
        k.make_public()
        os.remove(file)                                                                        
        print '[+] Deleting file ', file
```
Run
===
Craete MySQL tables:
```sh
python create_db_tables.py
```
Run the script
```sh
python main.py
```
