from selenium import webdriver
from tor_webdriver import tor_driver
from save import save_new_gifs
import time
from random import randint
from collections import deque


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
                     'cat.fr.eu.criteo', 'doubleclick',
                     'cat.nl.eu.criteo.com/delivery', 'adstore_icon_on.png',
                     'xblasterads']

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
        if all(j not in i for j in not_ad_images):
            final_gifs.add(i)

    driver.quit()
    tor_driver()[1].stop()
    return final_gifs


if __name__ == '__main__':

    # url_list = ['http://www.sigmalive.com', 'http://politis.com.cy',
    #             'http://www.24h.com.cy/', 'http://www.alfanews.com.cy/',
    #             'http://www.ant1iwo.com/', 'http://www.balla.com.cy/',
    #             'http://www.i-eidisi.com/', 'http://www.ilovestyle.com/',
    #             'http://www.kathimerini.com.cy/', 'http://www.kerkida.net/',
    #             'http://www.omonoia24.com/', 'http://www.onlycy.com/',
    #             'http://www.philenews.com/', 'http://www.stockwatch.com.cy/',
    #             'http://www.timeoutcyprus.com/', 'http://tvonenews.com.cy/',
    #             'http://cyprustimes.com/', 'http://www.24sports.com.cy/',
    #             'https://www.ergodotisi.com/', 'http://offsite.com.cy/',
    #             'http://showbiz.com.cy/', 'http://protathlima.com/',
    #             'http://www.tothemaonline.com/', 'http://shootandgoal.com/'
    #             ]

    with open('url_list.txt', 'r') as f:
        url_list = f.read().splitlines()

    while True:
        for url in url_list:
            if 'eidisi' in url or True:
                print '[+] Retrieving Gifs in URL: ', url
                gifs_url = find_static_files(url)
                print '[+] All Gif links', gifs_url
                save_new_gifs(gifs_url, url)

        time.sleep(randint(1200, 1800))
