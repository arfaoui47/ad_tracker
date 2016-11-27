from selenium import webdriver
from tor_webdriver import tor_driver
from selenium.webdriver.support.ui import WebDriverWait
from save import save_new_gifs
import requests
import time
from random import randint
from collections import deque


def r_iframe_lookup(driver, li, imgs):
    while len(li) > 0:
        iframe = li.popleft()
        try:
            print '[+]', iframe.get_attribute('ID')
            driver.switch_to_frame(iframe)

            images_tags = driver.find_elements_by_tag_name("img")
            imgs_src = [w.get_attribute('SRC') for w in images_tags]
            imgs += imgs_src
            try:
                iframe_list = driver.find_elements_by_tag_name('iframe')
                dq = deque(iframe_list)
                r_iframe_lookup(driver, dq, imgs)
            except:
                raise
            finally:
                driver.switch_to_default_content()
        except:
            pass
    return imgs


def iframe_get_gifs_urls(url):
    driver = webdriver.Firefox(executable_path='./geckodriver')
    driver.get(url)
    gifs_urls = set()
    final_gifs = set()
    imgs = []
    not_ad_images = ['www.google.com/ads/measurement/', 'gstatic',
                     'cat.fr.eu.criteo', 'doubleclick',
                     'cat.nl.eu.criteo.com/delivery', 'adstore_icon_on.png']

    xpaths = ["//iframe[contains(@id, 'google_ads_iframe_')]",
              "//iframe[contains(@src, 'http://ads.adstore.com.cy/')]",
              "//iframe[contains(@id, 'cdxhd_ifr')]"]

    for xpath in xpaths:
        iframes = driver.find_elements_by_xpath(xpath)
        if len(iframes) > 0:
            dq = deque(iframes)
            gifs_urls |= set(r_iframe_lookup(driver, dq, imgs))

    try:
        img_tags = driver.find_elements_by_xpath(
            "//img[contains(@SRC, 'http://www.easyenergy.com.cy/openx/www/images/')]")
        gifs_urls |= set([i.get_attribute('SRC') for i in img_tags])
    except:
        raise

    for i in gifs_urls:
        if all(j not in i for j in not_ad_images):  # some images are
            final_gifs.add(i)

    driver.quit()
    # tor_driver()[1].stop()
    return final_gifs


if __name__ == '__main__':
    now = int(time.time() * 1000)
    url_list = ['http://www.sigmalive.com', 'http://politis.com.cy',
                'http://www.24h.com.cy/', 'http://www.alfanews.com.cy/',
                'http://www.ant1iwo.com/', 'http://www.balla.com.cy/',
                'http://www.i-eidisi.com/', 'http://www.ilovestyle.com/',
                'http://www.kathimerini.com.cy/', 'http://www.kerkida.net/',
                'http://www.omonoia24.com/', 'http://www.onlycy.com/',
                'http://www.philenews.com/', 'http://www.stockwatch.com.cy/',
                'http://www.timeoutcyprus.com/', 'http://tvonenews.com.cy/',
                'http://cyprustimes.com/', 'http://www.24sports.com.cy/',
                'https://www.ergodotisi.com/', 'http://offsite.com.cy/',
                'http://showbiz.com.cy/', 'http://protathlima.com/'
                ]

    # driver = tor_driver()[0]
    # driver.get("https://check.torproject.org/")
    # time.sleep(5)
    # driver.quit()
    # tor_driver()[1].stop()

    while True:
        for url in url_list:
            print '[+] Retrieving Gifs in URL: ', url
            gifs_url = iframe_get_gifs_urls(url)
            print '[+] All Gif links', gifs_url
            save_new_gifs(gifs_url, url)
        time.sleep(randint(1200, 1800))
