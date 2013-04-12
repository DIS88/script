#-*- coding:utf-8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import Request, urlopen

def youknowed():
#    sock = urlopen('http://zh.wikipedia.org/wiki/水手').read().decode('utf-8','ignore')
#    reponse = urlopen(req)
    url = 'http://zh.wikipedia.org/wiki/水手'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22'}
    req = Request(url, headers=headers)
    res = urlopen(req)
    
    soup = BeautifulSoup(res.read())
    p = soup.find('p').renderContents()
    print  p
    
if __name__ == '__main__':
    youknowed()