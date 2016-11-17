# ad_tracker
[![Build Status](https://travis-ci.com/arfaoui47/ad_tracker.svg?token=CH8XvMgBpfMsqsoWSUb5&branch=master)](https://travis-ci.com/arfaoui47/ad_tracker)


Requirements
============

* Python 2.7 
* Works on Linux, Windows, Mac OSX, BSD
* Firefox >~ 48.0 version

Install
=======
Install Python requirements
```sh  
pip install -r requirements.txt
``` 
Install Tor and Privoxy
```sh
sudo apt-get install tor privoxy
```  
Set Privoxy to forward through Tor::
```sh
echo 'echo "forward-socks5 / localhost:9050 ." >> /etc/privoxy/config' | sudo -s
```
Run
===
```sh
python main.py
```
