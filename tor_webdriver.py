#Import webdriver from the selenium library
from selenium import webdriver

#Import the Proxy class from the selenium library
from selenium.webdriver.common.proxy import *

#Build the Proxy object using the locally running Privoxy


port = "8118" #The Privoxy (HTTP) port
myProxy = "127.0.0.1:"+port
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'ftpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': ''
})

def tor_driver():
	return webdriver.Firefox(proxy=proxy)

if __name__ == '__main__':
	driver = tor_driver()
	driver.get("http://www.ipligence.com/geolocation")