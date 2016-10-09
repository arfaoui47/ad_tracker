import requests
from hashlib import md5
import MySQLdb
import string 
import random
import os

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
	if url[:-3]=='jpg':
		extension='jpg'
	elif url[:-3]=='jpeg':
		extension='jpeg'
	elif url[:-3]=='png':
		extension='png'
	name = file_name_generator()
	file_name = name+'.'+extension
	with open(file_name,'wb') as f:
		f.write(requests.get(url).content)
	print '[+] Saving Gif to ', file_name
	f.close()
	return file_name

def data_insert(data, connexion):
	cursor = connexion.cursor()
	try:
		cursor.execute("INSERT INTO images(`checksum`) VALUES ({})".format(`data`))
		print '[+] Saving to MySQL database ...'
		connexion.commit()
	except:
		print '[-] Fail to save to DB !'
		connexion.rollback()

def to_md5(file):
	f=open(file, 'rb').read()
	check_sum = md5(f).hexdigest()
	print '[+] hashing file to md5: ', check_sum
	os.remove(file)    	 		
	print '[+] Deleting file ', file		#remove file  
	return check_sum

def save_new_gifs(urls):
	conn = db_connection()
	for url in urls:
		if 'tpc' in url:
			print '[+] checking for gif: ', url
			file = image_local_save(url);
			md5_hash = to_md5(file)

			if data_retrieve(md5_hash, conn):
				data_insert(md5_hash, conn)
			else:
				print '[-] Data is already in database'


if __name__ == '__main__':
	#urls = ['https://tpc.googlesyndication.com/simgad/1751857741877065419']
	urls = ['https://tpc.googlesyndication.com/simgad/8537187466804554545']
	save_new_gifs(urls)