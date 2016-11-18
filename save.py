from hashlib import md5
from upload_to_S3 import upload_to_S3
import requests
import MySQLdb
import string 
import random
import os
import time



def file_name_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def db_connection():
	connexion = MySQLdb.connect(host= "localhost",
                  		   user="root",
                  		   passwd="arfa47",
                  		   db="ad_tracker")
	return connexion


def data_retrieve(data, connexion):
	cursor = connexion.cursor()
	cursor.execute("select * from images where checksum={}".format(`data`))
	result = cursor.fetchall()
	print '[+] retrieving data ...'
	return True if len(result)==0 else False

def image_local_save(url):
	print '[+] Url to save: ', url
	extension = 'gif'
	if url[-3:]=='jpg':
		extension='jpg'
	elif url[-4:]=='jpeg':
		extension='jpeg'
	elif url[-3:]=='png':
		extension='png'
	name = file_name_generator()
	file_name = 'local_images/' + name + '.' + extension
	with open(file_name,'wb') as f:
		MAX_TRY = 6
		try_num = 1
		img_content = ''
		while try_num <= MAX_TRY and not img_content:
			try: 
				img_content = requests.get(url).content
			except:
				time.sleep(3)
				try_num += 1
				print '[-] Retreiving gifs, Retry number: ', try_num

		if img_content:
			f.write(img_content)
		else:
			print '[-] Enable to save gif'
			return 0
	print '[+] Saving Gif to ', file_name
	f.close()
	return file_name

def data_insert(data, connexion):
	cursor = connexion.cursor()
	try:
		cursor.execute("INSERT INTO images(checksum, date_creation) VALUES ({},{})".format(
			`data`, `time.strftime('%Y-%m-%d %H:%M:%S')`))
		print '[+] Saving to MySQL database ...'
		connexion.commit()
	except:
		print '[-] Fail to save to DB !'
		connexion.rollback()

def to_md5(file):
	f=open(file, 'rb').read()
	check_sum = md5(f).hexdigest()
	print '[+] hashing file to md5: ', check_sum
	return check_sum
	

def get_all_images(urls):
	pass
	


def save_new_gifs(urls):
	conn = db_connection()
	for url in urls:
		# if 'tpc' in url:
		file = image_local_save(url);
		if file:
			md5_hash = to_md5(file)
			upload_to_S3(md5_hash, file)
			if data_retrieve(md5_hash, conn):
				data_insert(md5_hash, conn)
			else:
				print '[-] Data is already in database'
			print


if __name__ == '__main__':
	#urls = ['https://tpc.googlesyndication.com/simgad/1751857741877065419']
	# urls = ['https://tpc.googlesyndication.com/simgad/8537187466804554545']
	urls = ['http://ds.serving-sys.com/BurstingRes///Site-83489/Type-0/768420c0-8760-431a-ad87-3b79c160c867.jpg']
	save_new_gifs(urls)