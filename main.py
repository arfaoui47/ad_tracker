from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from lxml import html, etree
import urllib
from save import save_new_gifs


def get_gifs_urls(url, iframes):
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



if __name__ == '__main__':
	url_list = ['http://www.sigmalive.com', 'http://politis.com.cy']
	iframes = {
			'http://www.sigmalive.com':['//*[@id="google_ads_iframe_/45099537/Leaderboard_0"]',
										'//*[@id="google_ads_iframe_/45099537/Main_Leaderboard_B_0"]', 
										'//*[@id="google_ads_iframe_/45099537/Main_Leaderboard_C_0"]', 
										'//*[@id="google_ads_iframe_/45099537/Main_Leaderboard_D_0"]', 
										'//*[@id="google_ads_iframe_/45099537/MainSkinLeft_0"]',
										'//*[@id="google_ads_iframe_/45099537/Main_G_0"]',
										'//*[@id="google_ads_iframe_/45099537/Main_C_0"]'
									   ],
			'http://politis.com.cy': ['//*[@id="google_ads_iframe_/110403327/POLITIS_728x90_02_0"]',
									  '//*[@id="google_ads_iframe_/110403327/300x250_01_0"]',
									  '//*[@id="google_ads_iframe_/110403327/300x250_03_0"]',
									  '//*[@id="google_ads_iframe_/110403327/POLITIS_728x90_03_0"]',
									  '//*[@id="google_ads_iframe_/110403327/300x250_06_0"]',
									  '//*[@id="google_ads_iframe_/110403327/SPT_300x250_02_0"]',
									  '//*[@id="google_ads_iframe_/110403327/300x250_07_0"]',
									  '//*[@id="google_ads_iframe_/110403327/SPT_300x250_02_0"]',
									 ]
			  }

	for url in url_list:
		print '[+] Retrieving Gifs in URL: ',url
		gifs_url = get_gifs_urls(url, iframes[url])
		print '[+] All Gif links',gifs_url	
		save_new_gifs(gifs_url)