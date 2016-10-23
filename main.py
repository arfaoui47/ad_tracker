from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lxml import html, etree
import urllib
from save import save_new_gifs
import requests
import time

def iframe_get_gifs_urls(url, iframes):
	driver = webdriver.Firefox()
	driver.get(url)
	gifs_urls = set()
	for iframe in iframes:
		try:
			print '[+] iframe:',iframe
			frame_found = WebDriverWait(driver, 10).until(lambda driver:driver.find_element_by_xpath(iframe))
			driver.switch_to_frame(frame_found)
			result =  driver.page_source
			# print result
			tree = html.fromstring(str(result.encode('utf-8')))
			imgs=tree.xpath('//img/@src')
			print "########", imgs  							 # for debugging 
			for i in imgs:
				if 'www.google.com/ads/measurement/' not in i and 'gstatic' not in i:   #some images are 
					gifs_urls.add(i)
			driver.switch_to_default_content()
		except Exception, e:
			print '[-] iframe fialed: ', iframe
			print '[-] Exception: ', str(e)
	driver.close()
	return gifs_urls


def subiframe_get_gifs_urls(url, iframes):
	driver = webdriver.Firefox()
	driver.get(url)
	gifs_urls = []
	for iframe in iframes:
		try:
			print '[+] iframe:',iframe
			first_iframe, second_iframe, third_iframe = iframe
			
			frame_found1 = WebDriverWait(driver, 10).until(lambda driver:driver.find_element_by_xpath(first_iframe))
			driver.switch_to_frame(frame_found1)
			result1 = driver.page_source

			tree1 = html.fromstring(str(result1.encode('utf-8')))
			time.sleep(1)
			frame_found2 = WebDriverWait(driver, 10).until(lambda driver:driver.find_element_by_xpath(second_iframe))
			driver.switch_to_frame(frame_found2)
			result2 = driver.page_source
			tree2 = html.fromstring(str(result2.encode('utf-8')))
		
			# time.sleep(1)
			# frame_found3 = WebDriverWait(driver, 10).until(lambda driver:driver.find_element_by_xpath(third_iframe))
			# driver.switch_to_frame(frame_found3)
			# result3 = driver.page_source
			# print '++++++++++',result3
			# tree3 = html.fromstring(str(result3.encode('utf-8')))

			imgs=tree2.xpath('//img/@src')
			print "########", imgs  							 # for debugging 
			for i in imgs:
				if 'www.google.com/ads/measurement/' and '//www.gstatic.com' not in i:   #some images are 
					gifs_urls.append(i)
			driver.switch_to_default_content()
			driver.switch_to_default_content()
			
		except Exception, e:
			print '[-] iframe fialed: ', iframe
			print '[-] Exception: ', str(e)
	driver.close()
	return gifs_urls

def sub_subiframe_get_gifs_urls(url, iframes):					# 3 steps iframes
	driver = webdriver.Firefox()
	driver.get(url)
	gifs_urls = []
	for iframe in iframes:
		try:
			print '[+] iframe:',iframe
			first_iframe, second_iframe, third_iframe = iframe
			
			frame_found1 = WebDriverWait(driver, 10).until(lambda driver:driver.find_element_by_xpath(first_iframe))
			driver.switch_to_frame(frame_found1)
			result1 = driver.page_source
			print '111111      ', result1
			tree1 = html.fromstring(str(result1.encode('utf-8')))
			time.sleep(1)
			frame_found2 = WebDriverWait(driver, 10).until(lambda driver:driver.find_element_by_xpath(second_iframe))
			driver.switch_to_frame(frame_found2)
			result2 = driver.page_source
			print '222222222       ', result2
			tree2 = html.fromstring(str(result2.encode('utf-8')))
			
			frame_found3 = WebDriverWait(driver, 10).until(lambda driver:driver.find_element_by_xpath(third_iframe))
			driver.switch_to_frame(frame_found3)
			result3 = driver.page_source
			print '3333333      ',result3
			tree3 = html.fromstring(str(result3.encode('utf-8')))

			frame_found4 = WebDriverWait(driver, 10).until(lambda driver:driver.find_element_by_tag_name('iframe'))
			print frame_found4
			driver.switch_to_frame(frame_found4)
			result3 = driver.page_source
			print '44444      ',result3
			tree3 = html.fromstring(str(result3.encode('utf-8')))

			imgs=tree3.xpath('//img/@src')
			print "########", imgs  							 # for debugging 
			for i in imgs:
				if 'www.google.com/ads/measurement/' and '//www.gstatic.com' not in i:   #some images are 
					gifs_urls.append(i)
			driver.switch_to_default_content()
			driver.switch_to_default_content()
			
		except Exception, e:
			print '[-] iframe fialed: ', iframe
			print '[-] Exception: ', str(e)
	driver.close()
	return gifs_urls


def easyenergy_get_gifs_url(url, urls):
	return urls

def images_in_source(url, paths):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	imgs = []
	for path in paths:
		imgs+=tree.xpath('//img[contains(@src, {})]/@src'.format(`path`))
	for i in imgs:
		if i[0] == '/':
			imgs.append(url+i)
			imgs.remove(i)
	return imgs


if __name__ == '__main__':
	now = int(time.time() * 1000)
	url_list = ['http://www.sigmalive.com', 'http://politis.com.cy', 'http://www.24h.com.cy/',
				'http://www.alfanews.com.cy/', 'http://www.ant1iwo.com/', 'http://www.balla.com.cy/',
				'http://www.i-eidisi.com/', 'http://www.ilovestyle.com/', 'http://www.kathimerini.com.cy/',
				'http://www.kerkida.net/','http://www.omonoia24.com/', 'http://www.onlycy.com/',
				'http://www.philenews.com/', 'http://www.stockwatch.com.cy/', 'http://www.timeoutcyprus.com/',
				'http://tvonenews.com.cy/'
				]
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
										},
			'http://www.ant1iwo.com/': {'urls':
									  ['//*[@id="google_ads_iframe_/126701466/Home_Page_Banner_300x250_4_0"]',
									  '//*[@id="google_ads_iframe_/126701466/Home_Page_Banner_768x90_1_0"]',
									  '//*[@id="google_ads_iframe_/126701466/Home_Page_Banner_Sponsored1_250x326_0"]',
									  '//*[@id="google_ads_iframe_/126701466/Home_Page_Banner_300x250_1_0"]',
									  '//*[@id="google_ads_iframe_/126701466/Home_Page_Banner_768x90_3_0"]',
									 ],
									 'type':'google_iframe'
									 },
			'http://www.balla.com.cy/': {'urls':
										   [
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=61',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=21',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=72',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=23',
										   'http://www.easyenergy.com.cy/openx/www/delivery/avw.php?zoneid=20',
											],
										'type': 'easyenergy'
										},
			'https://www.ergodotisi.com/': {'urls':
									  ['//*[@id="google_esf"]'									  
									 ],
									 'type':'google_iframe'
									 },
			'http://www.i-eidisi.com/': {'urls':
										   ['http://www.i-eidisi.com/wp-content/ttprsu'],
										'type': 'image_in_source'
										},
			'http://www.ilovestyle.com/': {'urls':
									  ['//*[@id="google_ads_iframe_Home_960x90"]',
									   '//*[@id="google_ads_iframe_/9520043/Home_undeslideshow_720x90_0"]',
									   '//*[@id="google_ads_iframe_RightSkinSlot"]',
									   '//*[@id="google_ads_iframe_LeftSkinSlot"]',
									   '//*[@id="google_ads_iframe_/9520043/HomePage_300x250_1_0"]',
									   '//*[@id="google_ads_iframe_/9520043/HomePage_300x250_2_0"]',
									   '//*[@id="google_ads_iframe_/9520043/HomePage_300x250_3_0"]',
									   '//*[@id="google_ads_iframe_HomePage_300x250_4"]',
									   '//*[@id="google_ads_iframe_HomePage_300x250_5"]',
									   '//*[@id="google_ads_iframe_/9520043/home_300x250_nexttocatwalks_0"]',
									 ],
									 'type':'google_iframe'
			 						 },
			'http://www.kathimerini.com.cy/': {'urls':
									  ["//iframe[contains(@src, 'http://ads.adstore.com.cy/__gb/?zonid=6&sizid=1&')]",
									   "//iframe[contains(@src, 'http://ads.adstore.com.cy/__gb/?zonid=6&sizid=2&')]",
									   "//iframe[contains(@src, 'http://ads.adstore.com.cy/__gb/?zonid=6&sizid=3&')]"
									 ],
									 'type':'google_iframe'},

			'http://www.kerkida.net/': {'urls':
									  ['//*[@id="google_ads_iframe_/38893584/kerkida_fp_1_0"]',
									   '//*[@id="google_ads_iframe_/38893584/kerkida_fp_2_0"]',
									   '//*[@id="google_ads_iframe_/38893584/kerkida_fp_3_0"]',
									   '//*[@id="google_ads_iframe_/38893584/kerkida_fp_4_0"]',
									   '//*[@id="google_ads_iframe_/38893584/kerkida_fp_5_0"]',
									   '//*[@id="google_ads_iframe_/38893584/kerkida_fp_6_0"]',
									   '//*[@id="google_ads_iframe_/38893584/kerkida_fp_7_0"]',
									   '//*[@id="google_ads_iframe_/38893584/kerkida_fp_8_0"]',
									   '//*[@id="google_ads_iframe_/38893584/kerkida_fp_9_0"]',
									   '//*[@id="google_ads_iframe_/38893584/kerkida_fp_10_0"]',
									   '//*[@id="google_ads_iframe_/38893584/kerkida_fp_11_0"]',
									 ],
									 'type':'google_iframe'},
			'http://www.omonoia24.com/': {'urls':
									  [
									  ('//*[@id="aswift_0"]', '//*[@id="google_ads_frame1"]', '//*[@id="ad_iframe"]'),
									  ('//*[@id="aswift_1"]', '//*[@id="google_ads_frame2"]', '//*[@id="ad_iframe"]'),
									  ],
									  'type':'google_sub_iframes'
									 },
			'http://www.onlycy.com/': {'urls':
									  ['//*[@id="google_ads_iframe_/38893584/onlycy_new_fp_1_0"]',
									   '//*[@id="google_ads_iframe_/38893584/onlycy_new_fp_2_0"]',
									   '//*[@id="google_ads_iframe_/38893584/onlycy_new_ap_3_0"]',
									   '//*[@id="google_ads_iframe_/38893584/onlycy_new_fp_5_0"]',
									 ],
									 'type':'google_iframe'},	
			'http://www.philenews.com/': {'urls':
									  [('//iframe[@id="cdxhd_ifr_159187_10"]', '//iframe[@id="aswift_0"]', '//iframe[@name="google_ads_frame1"]')

									  # '//*[@id="cdxhd_ifr_159183_5"]',
									  # '//*[@id="cdxhd_ifr_159187_3"]',
									   
									   # '//*[@id="google_ads_iframe_/38893584/onlycy_new_ap_3_0"]',
									   # '//*[@id="google_ads_iframe_/38893584/onlycy_new_fp_5_0"]',
									 ],
									 'type':'sub_sub_google_iframe'},
			'http://www.stockwatch.com.cy/': {'urls':
									  ['//*[@id="google_ads_iframe_/95309258/sw_home_tbr_0"]',
									   '//*[@id="google_ads_iframe_/95309258/sw_home_tbl_0"]',
									   '//*[@id="google_ads_iframe_/95309258/sw_home_bl1_0"]',
									   '//*[@id="google_ads_iframe_/95309258/sw_home_bl2_0"]',
									   '//*[@id="google_ads_iframe_/95309258/sw_home_bbl_0"]',
									   
									 ],
									 'type':'google_iframe'},

			'http://www.timeoutcyprus.com/': {'urls':
									  ['//*[@id="google_ads_iframe_HTML:728X90_HEADER_HOME"]',
									   '//*[@id="google_ads_iframe_HTML:300X250_TOP_RIGHT_HOME"]',
									   '//*[@id="google_ads_iframe_HTML:300X250_MIDDLE_RIGHT_HOME"]',
									   '//*[@id="google_ads_iframe_HTML:300X250_BOTTOM_RIGHT_HOME"]',
									   '//*[@id="google_ads_iframe_/7264676/300x600_sidebar_home_0"]',
									   '//*[@id="google_ads_iframe_sidebar_middle_home_300x250"]',

									   
									 ],
									 'type':'google_iframe'},
			'http://tvonenews.com.cy/': {'urls':
									  ['//*[@id="google_ads_iframe_/17337359/Slot1_0"]',
									   '//*[@id="google_ads_iframe_/17337359/Slot2_0"]',
									   '//*[@id="google_ads_iframe_/17337359/Slot3_0"]',
									   '//*[@id="google_ads_iframe_/17337359/Slot7_0"]',
									   '//*[@id="google_ads_iframe_/17337359/Slot8_0"]',
									   '//*[@id="google_ads_iframe_/17337359/Slot9_0"]',
									   '//*[@id="google_ads_iframe_/17337359/Slot10_0"]',
									 ],
									 'type':'google_iframe'},
}


	for url in url_list:
		print '[+] Retrieving Gifs in URL: ',url
		if gifs_paths[url]['type'] == 'sub_sub_google_iframe':
			gifs_url = sub_subiframe_get_gifs_urls(url, gifs_paths[url]['urls'])
			print '[+] All Gif links',gifs_url	
			save_new_gifs(gifs_url)
		if gifs_paths[url]['type'] == 'google_sub_iframes':
			gifs_url = subiframe_get_gifs_urls(url, gifs_paths[url]['urls'])
			print '[+] All Gif links',gifs_url	
			save_new_gifs(gifs_url)
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
	