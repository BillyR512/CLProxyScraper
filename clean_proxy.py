from gevent import monkey
monkey.patch_all()

from bs4 import BeautifulSoup
import requests
import timeit
from random import randrange as r


import gevent
import sys
import re
import time
import os
import string

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36'}

tmp = []
prox = []

def clean():
    """
    Tests all proxies from proxies.txt to craigslist.org and removes all proxies that do not pass from proxies.txt. Run by  "python clean_proxy.py"
    """
    f = open('proxies.txt', 'r')
    for item in f:
        s = item.strip()
        if s not in tmp:
            tmp.append(s)
    f.close()
    print 'testing %s proxies' % len(tmp)
    try:
        test = [gevent.spawn(test_proxy, proxy) for proxy in tmp]
        gevent.joinall(test)
    except KeyboardInterrupt:
        sys.exit('[-] Ctrl-C caught, exiting')

    print '%i proxies passed' % len(prox)
    f = open('proxies.txt', 'w')
    for proxy in prox:
        f.write("%s\n" % proxy)
    print 'saved!'
    gevent.killall(test)
    f.close()


def test_proxy(proxy):
    if len(prox) < 30:
        try:
            html = requests.get(
                    'http://www.craigslist.org/about/sites',
                    headers = headers,
                    proxies = {'http':'http://'+proxy,
                            'https':'http://'+proxy},
                    timeout = 7)
            if len(html.text) > 100:
                prox.append(proxy)
                print "%s passed" % proxy
        except:
            print "error with proxy %s" % proxy


if __name__ == "__main__":
    clean()
