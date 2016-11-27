from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.proxy import *
import random


def LoadUserAgents(uafile):
    """
    uafile : string
        path to text file of user agents, one per line
    """
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1 - 1])
    random.shuffle(uas)
    return uas


sizes = [(750, 1334), (800, 600), (1080, 1920), (640, 1136), (640, 609),
         (320, 480), (1440, 2560), (768, 1280), (540, 960), (480, 800),
         (720, 1280), (720, 720), (360, 480), (480, 720), (768, 1024),
         (1536, 2048), (480, 800), (600, 1024), (540, 960), (200, 400),
         (1200, 1920)]

uas = LoadUserAgents("user_agents.txt")

port = "8118"                                           # The Privoxy (HTTP) port
myProxy = "127.0.0.1:" + port
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'ftpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': ''
})


class MockDisplay():
    def stop(self):
        return 1


def tor_driver():
    # User_agent = random.choice(uas)
    # resolution = random.choice(sizes)
    # print User_agent
    # print resolution
    # display = Display(visible=1, size=resolution)
    # display.start()
    # profile = webdriver.FirefoxProfile()
    # profile.set_preference("general.useragent.override", User_agent)
    # driver = webdriver.Firefox(profile, executable_path='./geckodriver', proxy=proxy)
    # driver.set_window_size(*resolution)
    return webdriver.Firefox(executable_path='./geckodriver'), MockDisplay()


# return driver, display


if __name__ == '__main__':
    driver = tor_driver()
    driver.get("http://www.ipligence.com/geolocation")
    driver = tor_driver()
    driver.get("https://check.torproject.org/")
