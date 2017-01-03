# from selenium import webdriver
from tor_webdriver import tor_driver
from save import save_new_gifs
import time
from random import randint
from collections import deque
from configparser import ConfigParser
from create_db_tables import db_connection, find_all_websites
import os


def r_iframe_lookup(driver, li, imgs):
    """
    recursive iframe lookup
    :param driver: Firefox webdriver
    :param li: list of iframes to loop through
    :param imgs: url of static files found in iframes
    :return:
    """
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


def find_static_files(url):
    """
    find all type of static files
    :param url: website to crawl
    :return:  list off all static file of a specific website
    """
    # driver = webdriver.Firefox(executable_path='./geckodriver')
    driver = tor_driver()[0]
    driver.get(url)
    gifs_urls = set()
    final_gifs = set()
    imgs = []
    not_ad_images = ['www.google.com/ads/measurement/', 'gstatic',
                     'cat.fr.eu.criteo', 'doubleclick', 'lg.php?',
                     'cat.nl.eu.criteo.com/delivery', 'adstore_icon_on.png',
                     'xblasterads', 'tags.bluekai', 'dpm.demdex.net/ibs:dpid',
                     'EMPTY_IMG.png', 'production.selectmedia.asia']

    ##########################################################################
    #                           ad file in source                            #
    ##########################################################################

    image_in_source_urls = {'https://www.ergodotisi.com/':
                            "//img[contains(@SRC, 'https://ergodotisi.blo"
                            "b.core.windows.net/banners/')]",

                            'http://www.i-eidisi.com/':
                                "//img[contains(@SRC, 'http://www.i-eidisi.com"
                                "/wp-content/ttprsu')]",

                            'http://www.alfanews.com.cy/':
                                "//img[contains(@SRC, 'http://www.alfanews.com"
                                ".cy/images/banners')]"}

    if url in image_in_source_urls:
        for url_static in image_in_source_urls:
            img_tags = driver.find_elements_by_xpath(
                image_in_source_urls[url_static])
            gifs_urls |= set([i.get_attribute('SRC') for i in img_tags])

    ##########################################################################
    #                           3rd-party ads                                #
    ##########################################################################

    xpaths = ["//iframe[contains(@id, 'google_ads_iframe_')]",
              "//iframe[contains(@src, 'http://ads.adstore.com.cy/')]",
              "//iframe[contains(@id, 'cdxhd_ifr')]"]

    for xpath in xpaths:
        iframes = driver.find_elements_by_xpath(xpath)
        if len(iframes) > 0:
            dq = deque(iframes)
            gifs_urls |= set(r_iframe_lookup(driver, dq, imgs))

    ##########################################################################
    #                            easyenergy ads                              #
    ##########################################################################

    try:
        img_tags = driver.find_elements_by_xpath(
            "//img[contains(@SRC, 'http://www.easyenergy.com.cy/openx/www/"
            "images/')]")
        gifs_urls |= set([i.get_attribute('SRC') for i in img_tags])
    except:
        raise

    for i in gifs_urls:
        if i is not None:
            if all(j not in i for j in not_ad_images):
                final_gifs.add(i)

    driver.quit()
    tor_driver()[1].stop()
    return final_gifs


def crawl():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    config = ConfigParser()
    config.read(os.path.join(dir_path, '../config.ini'))
    conn = db_connection(config)
    url_list = find_all_websites(conn)

    while True:
        for url in url_list:
            print '[+] Retrieving Gifs in URL: ', url
            gifs_url = find_static_files(url)
            print '[+] All Gif links', gifs_url
            save_new_gifs(gifs_url, url)

        time.sleep(randint(1200, 1800))


if __name__ == '__main__':
    crawl()
