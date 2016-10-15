from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lxml import html, etree
import urllib
from save import save_new_gifs
import requests


def iframe_get_gifs_urls(url, iframes):
	driver = webdriver.Firefox()
	driver.get(url)
	gifs_urls = []
	for iframe in iframes:
		try:
			print '[+] iframe:',iframe
			frame_found = WebDriverWait(driver, 10).until(lambda driver:driver.find_element_by_xpath(iframe))
			driver.switch_to_frame(frame_found)
			result =  driver.page_source
			tree = html.fromstring(str(result.encode('utf-8')))
			
			imgs=tree.xpath('//img/@src')
			for i in imgs:
				if 'www.google.com/ads/measurement/' not in i:   #some images are 
					gifs_urls.append(i)
			driver.switch_to_default_content()
		except:
			print '[-] iframe fialed: ', iframe
	driver.close()
	return gifs_urls


def easyenergy_get_gifs_url(url, urls):
	return urls

def images_in_source(url, paths):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	imgs = []
	for path in paths:
		imgs+=tree.xpath('//img[contains(@src, "banners")]/@src')
	for i in imgs:
		if i[0] == '/':
			imgs.append(url+i)
			imgs.remove(i)
	return imgs
	

if __name__ == '__main__':
	url_list = ['http://www.sigmalive.com', 'http://politis.com.cy', 'http://www.24h.com.cy/',
				'http://www.alfanews.com.cy/']
	gifs_paths = {
			'http://www.sigmalive.com':{'urls':
										['//*[@id="google_ads_iframe_/45099537/Leaderboard_0"]',
										'//*[@id="google_ads_iframe_/45099537/Main_Leaderboard_B_0"]', 
										'//*[@id="google_ads_iframe_/45099537/Main_Leaderboard_C_0"]', 
										'//*[@id="google_ads_iframe_/45099537/Main_Leaderboard_D_0"]', 
										'//*[@id="google_ads_iframe_/45099537/MainSkinLeft_0"]',
										'//*[@id="google_ads_iframe_/45099537/Main_G_0"]',
										'//*[@id="google_ads_iframe_/45099537/Main_C_0"]'
									   ],
									   'type':'google_iframe'
									   },
			'http://politis.com.cy': {'urls':
									  ['//*[@id="google_ads_iframe_/110403327/POLITIS_728x90_02_0"]',
									  '//*[@id="google_ads_iframe_/110403327/300x250_01_0"]',
									  '//*[@id="google_ads_iframe_/110403327/300x250_03_0"]',
									  '//*[@id="google_ads_iframe_/110403327/POLITIS_728x90_03_0"]',
									  '//*[@id="google_ads_iframe_/110403327/300x250_06_0"]',
									  '//*[@id="google_ads_iframe_/110403327/SPT_300x250_02_0"]',
									  '//*[@id="google_ads_iframe_/110403327/300x250_07_0"]',
									  '//*[@id="google_ads_iframe_/110403327/SPT_300x250_02_0"]',
									 ],
									 'type':'google_iframe'
									 },
			'http://www.24h.com.cy/': {'urls':
										   ['http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=4',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=10',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=66',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=18',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=78',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=79',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=19',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=75',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=76',
											],
										'type': 'easyenergy'
										},
			'http://www.alfanews.com.cy/': {'urls':
										   ['http://www.alfanews.com.cy/images/banners'],
										'type': 'image_in_source'
										}

			  }

	for url in url_list:
		print '[+] Retrieving Gifs in URL: ',url
		if gifs_paths[url]['type'] == 'google_iframe':
			gifs_url = iframe_get_gifs_urls(url, gifs_paths[url]['urls'])
			print '[+] All Gif links',gifs_url	
			save_new_gifs(gifs_url)
		if gifs_paths[url]['type'] == 'easyenergy':
			gifs_url = easyenergy_get_gifs_url(url, gifs_paths[url]['urls'])
			print '[+] All Gif links',gifs_url	
			save_new_gifs(gifs_url)
		if gifs_paths[url]['type'] == 'image_in_source':
			gifs_url = images_in_source(url, gifs_paths[url]['urls'])
			print '[+] All Gif links',gifs_url	
			save_new_gifs(gifs_url)