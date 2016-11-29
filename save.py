from hashlib import md5
import requests
import MySQLdb
import string
import random
import time
from configparser import ConfigParser
from upload_to_S3 import upload_to_S3
import os


config = ConfigParser()
config.read('conf.ini')


def file_name_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def db_connection():
    connexion = MySQLdb.connect(host=config.get('MySQL', 'host'),
                                user=config.get('MySQL', 'user'),
                                passwd=config.get('MySQL', 'password'),
                                db=config.get('MySQL', 'db'))

    return connexion


def data_retrieve(data, connexion):
    cursor = connexion.cursor()
    cursor.execute("select * from images where checksum={}".format(repr(data)))
    result = cursor.fetchall()
    print '[+] retrieving data ...'
    return True if len(result) == 0 else False


def image_local_save(url):
    print '[+] Url to save: ', url
    extension = 'gif'
    if url[-3:] == 'jpg':
        extension = 'jpg'
    elif url[-4:] == 'jpeg':
        extension = 'jpeg'
    elif url[-3:] == 'png':
        extension = 'png'
    name = file_name_generator()
    file_location = 'local_images/' + name + '.' + extension
    with open(file_location, 'wb') as f:
        MAX_TRY = 6
        try_num = 1
        img_content = ''
        while try_num <= MAX_TRY and not img_content:
            try:
                if url.split('/')[0] == 'data:image':
                    img_content = url.split(',')[1].decode('base64')
                else:
                    img_content = requests.get(url).content
            except:
                time.sleep(3)
                try_num += 1
                print '[-] Retreiving gifs, Retry number: ', try_num

        if img_content:
            f.write(img_content)
        else:
            print '[-] Enable to save gif'
            return {}
    print '[+] Saving Gif to ', file_location
    f.close()

    result = {
        'file_location': file_location,
        'extension': extension,
        'original_url': url}

    return result


def data_insert(md5_hash, data, website, url_bucket, connexion):
    cursor = connexion.cursor()
    try:
        if len(data['original_url']) < 500:
            original_url = str(data['original_url'])
        else:
            original_url = 'data:image'
        cursor.execute("INSERT INTO images(checksum, date_creation, url,"
                       " website, file_type, original_url) VALUES ({},{},{},{}"
                       ",{},{})".format(
                           repr(md5_hash),
                           repr(time.strftime('%Y-%m-%d %H:%M:%S')),
                           repr(url_bucket), repr(website),
                           repr(data['extension']),
                           repr(original_url)))

        print '[+] Saving to MySQL database ...'
        connexion.commit()
    except:
        raise
        print '[-] Fail to save to DB !'
        connexion.rollback()


def to_md5(file):
    f = open(file, 'rb').read()
    check_sum = md5(f).hexdigest()
    print '[+] hashing file to md5: ', check_sum
    return check_sum


def save_new_gifs(urls, website):
    conn = db_connection()

    for url in urls:
        data = image_local_save(url)
        file = data.get('file_location', 0)
        if file:
            md5_hash = to_md5(file)
            url_bucket = upload_to_S3(md5_hash, file)
            try:
                os.remove(file)
            except:
                pass
            if data_retrieve(md5_hash, conn):
                data_insert(md5_hash, data, website, url_bucket, conn)
            else:
                print '[-] Data is already in database'
            print


if __name__ == '__main__':
    urls = ['https://tpc.googlesyndication.com/simgad/8537187466804554545']
    save_new_gifs(urls, 'sigma')
