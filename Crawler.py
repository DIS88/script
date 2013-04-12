# -*- coding: utf-8 -*-

'''
Created on 2012-7-16

@author: zou
'''
from sgmllib import SGMLParser
import urllib
import sys
from datetime import datetime
import re

def usage():
    print "A simple crwaler "
    print "Usage: python crawler.py -site [...] -max_size [...] -o [outfiel path]"
    print "e.g: python crawler.py -site http://www.hao123.com -max_size 12 -to test.txt"
    sys.exit(1)

class Crawler(SGMLParser):
    def __init__(self, max_size, url):
        self.max_size = int(max_size)
        self.url = url
        if  len(url.split('http://www.'))==2:
            #www.a.com
            self.domain = url.split('http://www.')[1]
        else:
            #a.com
            self.domain = url.split('http://')[1]
        self.reset()
        
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []
        self.js = []
        self.css = []
        self.imgs = []
        
    def change_url(self, href):
        #return a dict
        if href:
            has_http = re.findall('http://', href[0])
            if not has_http:
                if  not href[0].startswith('#') and not href[0].startswith('javascript:'):
                    return [self.url + '/' + href[0]]
                else:
                    return None
            else:
                in_domain = re.findall(self.domain, href[0])
                if in_domain:
                    return href
                else:
                    return None
        
#   handle urls <a class="home" title="��ҳ" href="/">��ҳ</a>
    def start_a(self, attrs):
        if len(self.urls) < self.max_size:
            href = [v for k, v in attrs if k=='href']
            change_url = self.change_url(href)
            if change_url!= None:
                self.urls.extend(change_url)
#            if href:
#                has_http = re.findall('http://', href[0])
#                if not has_http and not href[0].startswith('#') and not href[0].startswith('javascript:'):
#                    self.urls.extend([self.url + '/' + href[0]])
#                else:
#                    in_domain = re.findall(self.domain, href[0])
#                    if in_domain:
#                        self.urls.extend(href)
         
    #handle css <link rel="stylesheet" href="/theme/inove/style.css" type="text/css" />   
    def start_link(self, attrs):
        href = [v for k, v in attrs if k=='href' and v.endswith('.css')]
        if href and self.change_url(href)!= None:
            self.css.extend(self.change_url(href))
    
    #handl js <script type="text/javascript" src="/dimg/js/jquery.form.utf8.js"></script>
    def start_script(self, attrs):
        src = [v for k, v in attrs if k=='src' and v.endswith('.js')]
        change_url = self.change_url(src)
        if change_url!= None:
            self.js.extend(change_url)
    
    #handle imgs <img alt="" src="{{ media_url }}img/information/menu7.jpg" />
    def start_img(self, attrs):
        src = [v for k, v in attrs if k=='src']
        change_url = self.change_url(src)
        if change_url!= None:
            self.imgs.extend(change_url)
#        if src:
#            has_http = re.findall('http://', src[0])
#            if not has_http:
#                self.imgs.extend([self.url + '/' + src[0]])
#            else:
#                in_domain = re.findall(self.domain, src[0])
#                if in_domain:
#                    self.imgs.extend(src)
            

def open_and_save(url, max_size, t_path):
    sock = urllib.urlopen(url)
#    domain = url.split('http://www')[1]
    res = sock.read()
    crawler = Crawler(max_size, url=url)
    crawler.feed(res)
    t_file = open(t_path + str(datetime.now().minute), 'wb')
    t_file.write('Create at: %s  \n' % str(datetime.now())) 
    t_file.write('The urls:' + '\n') 
    for url in crawler.urls:
        t_file.write('\t' + url + '\n') 
    t_file.write('The js:' + '\n') 
    for js in crawler.js:
        t_file.write('\t' + js + '\n')
    t_file.write('The css:' + '\n')  
    for css in crawler.css:
        t_file.write('\t' + css + '\n' )
    t_file.write('The imgs:' + '\n')  
    for img in crawler.imgs:
        t_file.write('\t' + img + '\n') 
    t_file.close()
    print 'Finish'
            
if __name__ == '__main__':
    if '-site' not in sys.argv:
        usage()
    else:
        op_dict = {}
        op_dict['-max_size'] = 1000
        op_dict['-to'] = 'text.txt' 
        for i in range(len(sys.argv)):
            if sys.argv[i].startswith('-'):
                try:
                    op_dict[sys.argv[i]] = sys.argv[i+1]
                except IndexError:
                    print 'option %s need a result' % sys.argv[i]
                    sys.exit(1)
        open_and_save(op_dict['-site'], op_dict['-max_size'], op_dict['-to'])
