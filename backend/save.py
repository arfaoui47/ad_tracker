from hashlib import md5
import requests
import MySQLdb
import string
import random
import time
from configparser import ConfigParser
from upload_to_S3 import upload_to_S3, upload_dir_to_S3
import os


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
config = ConfigParser()
config.read(os.path.join(dir_path, '../config.ini'))


def file_name_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def db_connection():
    connexion = MySQLdb.connect(host=config.get('MySQL', 'host'),
                                user=config.get('MySQL', 'user'),
                                passwd=config.get('MySQL', 'password'),
                                db=config.get('MySQL', 'db'))

    return connexion


def adtracking_log(checksum, location, connexion):
    """
    track authorized adverts
    :param checksum:
    :param location: domain of advert location
    :param connexion:
    :return:
    """
    with connexion:
        cursor = connexion.cursor()
        cursor.execute("INSERT INTO adtracking(checksum, date_creation,"
                       " location) VALUES ({},{},{})".format(
                           repr(checksum),
                           repr(time.strftime('%Y-%m-%d %H:%M:%S')),
                           repr(location)))
        connexion.commit()
    print '[+] Saving tracked advert'


def create_screenshot(iframe):
    location = iframe.location
    size = iframe.size
    driver.save_screenshot('screenshot.png') # saves screenshot of entire page    
    im = Image.open('screenshot.png') # uses PIL library to open image in memory
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('screenshot.png') #

def create_folder_and_move_images(images):
    md5_list = []
    file_list = []
    for i in images:
        data = image_local_save(i)
        file = data.get('file_location', None)
        if file:
            md5_hash = to_md5(file)
            md5_list.append(md5_hash)
            file_list.append(file)
    hashlist = ''.join(md5_list)
    check_sum = md5(hashlist).hexdigest()
    os.makedirs(os.path.join(dir_path, 'local_images/', check_sum))
    for file in file_list:
        os.rename(os.path.join(dir_path, 'local_images/',file),
         os.path.join(dir_path, 'local_images/', check_sum, file))
    upload_dir_to_S3(os.path.join(dir_path, 'local_images/', check_sum))




def data_retrieve(md5_hash, location, connexion):
    """
    retrieve existing adverts that have authorized value of True and
    insert log in adtracking table
    :param md5_hash:
    :param connexion:
    :return: False if data is found and True if not
    """
    with connexion:
        print '[+] retrieving data ...'
        cursor = connexion.cursor()
        cursor.execute("select * from images where checksum={}"
                       .format(repr(md5_hash)))
        all_adverts = cursor.fetchall()
        if len(all_adverts) == 0:
            return True
        else:
            print '[-] file is already in database' 
        
        cursor.execute("select * from images where checksum={} "
                       "and authorized='True'".format(repr(md5_hash)))
        authorized_adverts = cursor.fetchall()
        if len(authorized_adverts) > 0:
            adtracking_log(md5_hash, location, connexion)
            return False


def image_local_save(url):
    """

    :param url:
    :return:
    """
    print '[+] Url to save: ', url
    extension = 'gif'
    if url[-3:] == 'jpg':
        extension = 'jpg'
    elif url[-4:] == 'jpeg':
        extension = 'jpeg'
    elif url[-3:] == 'png':
        extension = 'png'
    name = file_name_generator()
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    file_location = os.path.join(dir_path,'local_images/' + name + '.' + extension)
    with open(file_location, 'wb') as f:
        MAX_TRY = 3
        try_num = 1
        img_content = ''
        while try_num <= MAX_TRY and not img_content:
            try:
                if url.split('/')[0] == 'data:image':
                    # if image is coded to base 64 and providing an url
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


def data_insert(md5_hash, data, website, url_bucket, banner_size, connexion):
    """
    insert a row to image table if for new adverts
    :param md5_hash: checksum field in database
    :param data: dict that contain extension, original_url and file location
    :param website: domain name of advert location
    :param url_bucket: S3 url of saved advert
    :param connexion:
    :return:
    """
    cursor = connexion.cursor()
    try:
        if len(data.get('original_url', 0)) < 500:
            original_url = str(data['original_url'])
        else:
            original_url = 'data:image'
        date_creation = time.strftime('%Y-%m-%d %H:%M:%S')
        year = time.strftime('%Y')
        month = time.strftime('%d/%m/%Y')
        date = time.strftime('%Y%m%d')
        cursor.execute("INSERT INTO images(checksum, date_creation, year,"
                       " month, date, url, website, file_type, original_url,"
                       " authorized, banner_size) VALUES ({},{},{},{},{},{},{},{},{},{},{})"
                       .format(
                           repr(md5_hash),
                           repr(date_creation),
                           repr(year),
                           repr(month),
                           repr(date),
                           repr(url_bucket), repr(website),
                           repr(data.get('extension', 0)),
                           repr(original_url),
                           repr('NULL'),
                           repr(banner_size)))

        print '[+] Saving to MySQL database ...'
        connexion.commit()
    except:
        raise
        print '[-] Fail to insert data to DB !'
        connexion.rollback()



def to_md5(file):
    """

    :param file:
    :return:
    """
    f = open(file, 'rb').read()
    check_sum = md5(f).hexdigest()
    print '[+] hashing file to md5: ', check_sum
    return check_sum


def save_new_gifs(urls, website):
    """

    :param urls:
    :param website: domain of advert location
    :return:
    """
    conn = db_connection()

    for url, banner_size in urls:
        print url
        data = image_local_save(url)
        file = data.get('file_location', None)
        if file:
            md5_hash = to_md5(file)
            url_bucket = upload_to_S3(md5_hash, file)
            try:
                os.remove(file)
            except:
                pass
            if data_retrieve(md5_hash, website, conn):
                size = banner_size.split('x')
                if any(i < '5' for i in size):   # do not save advert if size is zero
                    continue
                data_insert(md5_hash, data, website, url_bucket, banner_size, conn)
            print

    conn.close()

if __name__ == '__main__':
    urls = ['https://tpc.googlesyndication.com/simgad/8537187466804554545',
            'https://tpc.googlesyndication.com/simgad/14401369669909578556',
            'https://tpc.googlesyndication.com/simgad/11150122043232262085',
            'https://tpc.googlesyndication.com/simgad/16091105791262164897']
    save_new_gifs(urls, 'test4.com')
