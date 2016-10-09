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
		frame_found = WebDriverWait(driver, 10).until(lambda driver:driver.find_element_by_xpath(iframe))
		driver.switch_to_frame(frame_found)
		result =  driver.page_source
		print '[+] Retrieving page source of: ',url
		tree = html.fromstring(str(result.encode('utf-8')))
		imgs=tree.xpath('//img/@src')
		gifs_urls+=imgs
	return gifs_urls



if __name__ == '__main__':
	url_list = ['http://www.sigmalive.com']
	iframes = {
			'http://www.sigmalive.com': ['//*[@id="google_ads_iframe_/45099537/Main_Leaderboard_B_0"]']
			  }

	for url in url_list:
		gifs_url = get_gifs_urls(url, iframes[url])
		print '[+] All Gifs links',gifs_url	
		save_new_gifs(gifs_url)