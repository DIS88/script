#-*-coding:utf-8 -*-
'''
Created on 2011-10-8

@author: zou
http://www.tianya.cn/bbs/  天涯社区
'''
from urllib import *
import urlparse
from BeautifulSoup import BeautifulSoup
import webbrowser
class  tianya(object):
    def __init__(self,url,nickname=None,title=None):
        self.start_url=url
        self.nickname=nickname
        self.current_url=url
        self.title=title
#        src=urlopen(url).read().decode('gbk','ignore')
#        soup=BeautifulSoup(url)
        self.counter=1
        self.author=None
    def __iter__(self):
        return self
    def next(self):
        print '正在分析第%s页内容'%self.counter
        print '分析页面',self.current_url
        print '-------------分割线--------------'
        '''天涯每页99条消息   posts.__len__==100-101'''
        if self.current_url is None:
            print 'finished Tianya'
            raise StopIteration
        src=urlopen(self.current_url).read().decode('gbk','ignore')
        soup=BeautifulSoup(src)
        content=[]
        posts=soup.findAll('div',{'class':'post','_app':'eleshare'})#99
        print 'postlen',posts.__len__()
        usertables=soup.findAll('table',{'bgcolor':'#f5f9fa'})#98
        print 'userlen',usertables.__len__()
        syndication={}
        syndication['url']=self.current_url
        syndication['content']=[]
        for i in range(usertables.__len__()):
            username=self.get_otheruser(usertables[i])
            if not self.author:
                self.author=self.get_nickname(soup)
            if not self.title:
                self.title=self.get_title(soup)
#            print 'self.author',self.author
            if username==self.author:
                content=self.get_content(posts[i+1])
                time=0
                syndication['content'].append({
                                            'post':content,
                                            'time':time
                                            })
        self.current_url=self.get_nexturl(soup)
        print 'self.current_url',self.current_url
        self.counter+=1
        return syndication
    def get_nickname(self,soup):
        '''
        <table cellspacing="0" cellpadding="0" id="firstAuthor">
<tr align="center">
<td align="center">作者：<a href="http://my.tianya.cn/name/jimher" target="_blank">jimher</a><span name="ad_logo_userid_10524080" value="10524080"></span> &nbsp;发表日期：2011-10-6 15:44:00</td>
<!--举报 fangxu 2010-8-20-->
</tr>
</table>'''
        name=soup.find('table',{'id':'firstAuthor'}).a.renderContents()#这个
        return name
    def get_content(self,post):
        content=post.renderContents().replace('<div class="post-jb"></div>','')
        return content
    def get_otheruser(self,usertable):
        username=usertable.a.renderContents()
        '''<table cellspacing="0" border="0" bgcolor="#f5f9fa" width="100%"><tr><td width="100" align="RIGHT" valign="bottom"></td><td><center><br /><font size="-1" color="green">作者：<a href="/browse/Listwriter.asp?vid=55930831&amp;vwriter=焖烧小马甲" target="_blank">焖烧小马甲</a><span name="ad_logo_userid_55930831" value="55930831"></span>　回复日期：2011-10-06　15:47:05</font>　</center></td><td width="100" align="RIGHT" valign="bottom">&nbsp;</td></tr></table>'''
        return username
    def get_title(self,soup):
        '''『<a href="http://www.tianya.cn/publicforum/articleslist/0/funinfo.shtml" target="_top">娱乐八卦</a>』 
        [八卦江湖]好奇怪的气氛啊！一个外国人死了，有一群那样的人各种伤感！看不懂！'''
        return soup.find('span',{'id':'adsp_content_title_left'}).parent.contents[1].renderContents()
    def get_nexturl(self,soup):
        next=soup.find(text=u'下一页')
        if next:
            return next.parent.get('href').decode('utf8') 
        return None
class Iterable(object):
    def __init__(self):
        self.counter = 0
    def __iter__(self):
        return self
    def next(self):
        if self.counter>10: # 如果计数器大于10，就停止迭代
            raise StopIteration()
        print 'get next, current is %d'%self.counter
        self.counter += 1 # 计数器增1
class Indexable(object):
    def __getitem__(self, i): # 定义__getitem__, 如果i 大于10，就停止迭代
        if i>10:
            raise StopIteration()
        print 'get object %d'%i
        
if __name__=='__main__':
    print '准备直播'
    #http://www.tianya.cn/publicforum/content/free/1/1776881.shtml   1
    #http://www.tianya.cn/publicforum/content/funinfo/1/2875855.shtml  N
    ty=tianya('http://www.tianya.cn/publicforum/content/free/1/1776881.shtml')
    counter=0
    file=open('tianya.html','w')
    file.write('''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><HTML><HEAD><META http-equiv=Content-type content="text/html; charset=utf-8">
<TITLE>tianya</TITLE>
<META http-equiv=Content-Type content="text/html; charset=utf-8"></head><body><table>''')
    for y in ty:
        file.write(ty.title)
        if not y["content"]:
            continue
        for detail in y['content']:
#            file.write('<tr><td>%s</td></tr>')%str(ty.counter)
            file.write('<tr><td>%(post)s</td></tr>'%detail)
            print ('<tr><td>%s</td></tr>')%str(ty.counter)
            print '%(post)s'%detail
    file.write('''</table></body>''')
    file.close()
    import webbrowser
    webbrowser.open_new('tianya.html')
