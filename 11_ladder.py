# -*- coding:utf-8 -*-
'''
Created on 2013-2-26
@author: zou
'''
import urllib2, os.path, urllib
import time
from urllib2 import urlopen, Request
import json
COOKIEFILE = 'cookies.libwww-perl' #www protocal libary for perl

try:
    import cookielib
except ImportError:
    cookielib = None
    try:
        import ClientCookie
    except ImportError:
        cj = None
    else:
        urlopen = ClientCookie.urlopen
        cj = ClientCookie.LWPCookieJar()    
        Request = ClientCookie.Request
else:
    cj = cookielib.LWPCookieJar()

#def install_cj():
if cj is not None:
    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE)
    if cookielib:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    else:
        opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
        ClientCookie.install_opener(opener)

from sgmllib import SGMLParser
class Fuck11(SGMLParser):
    def __init__(self):
        self.reset()
    
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []
        self.view_state = ''
        self.event_validation = ''
        
    def start_a(self, attrs):
        pass
            
    def start_input(self, attrs):
        dict_attrs = {}
        for k,v in attrs:
            dict_attrs[k] = v
        if 'name' in dict_attrs:
            if dict_attrs['name']=='__VIEWSTATE':
                self.view_state = dict_attrs['value']
            if dict_attrs['name']=='__EVENTVALIDATION':
                self.event_validation = dict_attrs['value']
#        self.view_state = [attrs['value'] for k,v in attrs if k=='name' and v=='__VIEWSTATE']
#        self.envent_validation = [attrs['value'] for k,v in attrs if k=='name' and v=='__EVENTVALIDATION']


username = 'get_ladder ' #uid=347783110
password = 'ladder123'
time_stamp = int(time.time()*1000)
u_name = 'turbogears' #
u_name =  'honey丶轩'
uid = 0
request_url = 'http://i.5211game.com/request/?r=%s' % time_stamp 
person_url = 'http://i.5211game.com/%s' % u_name
ladder_url = 'http://i.5211game.com/rating/ladder?u=%s' % uid  #旧版查询中心
login_url = 'http://passport.5211game.com/t/Login.aspx'
rating_url = 'http://i.5211game.com/request/rating/?r=%s' % time_stamp  #新版查询中心 

class Ladder(object):
    ''''''
    #这是专门建立的查询账号(和密码)
    USERNAME = 'get_ladder'
    PASSWORD = 'ladder123'
    def __init__(self, username):
        self._username = username
        self._userid = '' 
    
    def get_uid(self, username):
        return uid
    
    def _login(self):
        pass





def login_platform():
    try:
        sock = urllib.urlopen(login_url)
        result = sock.read()
        fk11 = Fuck11()
        fk11.feed(result)
        #fk11.view_state, fk11.envent_validation
        params = {}
        params['__VIEWSTATE'] = fk11.view_state
        params['__EVENTVALIDATION'] = fk11.event_validation
        params['txtUser'] = username
        params['txtPassWord'] = password
        params['butLogin'] = '登陆'
        params['UserCheckBox'] = 'on'
        data = urllib.urlencode(params)
        #headers = {'User-agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windowns NT)'}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22'}
        req = Request(login_url, data, headers)  
        reponse = urlopen(req)
    except IOError, e:
        print 'Fail to open "%s"' % login_url
        if hasattr(e, 'code'):
            print 'Error code: %s.' % e.code 
    else:
        print 'login_success', reponse.info()#, reponse.read()
        if cj is None:
            print "没有 cookie jar, 今天不能显示cookies"
        else:
            print '获得的cookies：'
            for index, cookies in enumerate(cj):
                print index, ':', cookies
            cj.save(COOKIEFILE) 
#        install_cj()
#        __VIEWSTATE = '' 
#        __EVENTVALIDATION = ''

def _post_rating_request(params):
    data = urllib.urlencode(params)
    rating_request = Request(rating_url, data)
    rating_response= urlopen(rating_request)
    result = rating_response.read()
    result = json.loads(result)
    
    return result


def get_uid_by_pname(u_name=u_name):
#    person_url = 'http://i.5211game.com/%s' % u_name
#    p_request = urlopen(person_url)
#    p_result = p_request.read()
#    print p_result
#    uid = re.findall(r"YY.d.j = (\d+)", p_result)[0]
    print '[*]XXX'
    params = {}
    params['method'] = 'getuidbypname'
    params['name'] = u_name
    data = urllib.urlencode(params)
    uid_request = Request(request_url, data)
    response = urlopen(uid_request)
    result = json.loads(response.read())
    if result['error']==1:
        print result['reinfo']
        return None
    return int(result['uid'])
    

def get_ladder_score():
    
    ladder_url = 'http://i.5211game.com/rating/ladder?u=%s' % uid  #旧版战绩中心 有ladder字样
    ladder_request = Request(ladder_url)
    ladder_response= urlopen(ladder_request)
#    if ladder_response.geturl()!=ladder_url:
    if not ladder_response.geturl().startswith('http://i.5211game.com/rating/'): #新版战绩中心 无ladder
        login_platform()
        ladder_request = Request(ladder_url)
        ladder_response= urlopen(ladder_request)
    result = ladder_response.read()
#    patterns = re.compile(r'YY.d.j = (\d+)')
#    re.findall(patterns, )
#    result = {}
#    result['score'] = '' 
#    result[''] = ''
#    result[''] = ''
#    result['uid'] = ''
    print ladder_response.geturl()
    return ladder_response.geturl()#,
     

def load_score(user_id):
    '''载入名将战绩'''
    ps = {}
    ps['method'] = 'loadscore'
    ps['type'] = 10001
    ps['uid'] = user_id
    result = _post_rating_request(ps)
    
    return result

def get_hero_score(user_id, hero_id):
    """03.04.22 返回空值"""
    ps = {}
    ps['method'] = 'getscore'
    ps['uid'] = user_id
    ps['heroId'] = hero_id
    result = _post_rating_request(ps)
    
    return result

def get_hero_list(user_id):
    ps = {}
    ps['method'] = 'ladderheros'
    ps['u'] = user_id
    ps['t'] = 10001
    result = _post_rating_request(ps)
#    rating_file = open('rating_%s.txt' % u_name, 'wb')
    print result.keys()
    heroRoadInfos = result['heroRoadInfos']
#    rating_file.write(heroRoadInfos + '\n')
    ratingHeros = result['ratingHeros']
    '''{u'heroassist': 37, u'win': 0, u'resv10': 2, u'p_mvp': u'0.0', u'p_heroassist': u'6.2', u'total': 6, u'use': 6, u'resv9': 0, u'resv8': 0, u'resv5': 0,
     u'heroname': u'\u672b\u65e5\u4f7f\u8005', u'resv7': 1, u'resv6': 0, u'score': 467, u'heroId': u'UC42', u'offline': 0, u'p_resv6': u'0.0', u'p_resv7': 
     u'0.2', u'p_resv5': u'0.0', u'p_resv8': u'0.0', u'p_resv9': u'0.0', u'p_win': u'0.00%', u'mvp': 0, u'lost': 6, u'r_win': u'0.00%',
      u'herotype': u'\u529b\u91cf', u'p_resv10': u'0.3'}'''
    for hero in ratingHeros:
        print hero['heroname'], hero['score'], hero['total'], hero['r_win']
#        rating_file.write(str(hero) + '\n')
#        for k,v in hero.items():
#        print hero['heroname'], hero['heroId'], hero['score'], 'rating_match:',  hero['total'], 'win_rating:', hero['r_win'], '英魂次:', hero['resv10']
        #, '场均英魂:', hero['p_resv10']
#    rating_file.close()
    print 'heroRoadInfos', heroRoadInfos
    
def get_rating(user_id):
    ps = {}
    ps['method'] = 'getrating'
    ps['u'] = user_id
    ps['t'] = 10001
    result = _post_rating_request(ps)
    ttInfos = result['ttInfos']#天梯信息
#    mjInfos = result['mjInfos']#名将信息 就不分析了。
    rating = result['rating']#天梯积分 2200
    rank = result['rank']#排名1550
#    rankInfos = result['rankInfos']#排名前十的狗币。
#    mjheroInfos = result['mjheroInfos']
#    tm = result['tm'] 他妈32?
    print result.keys()
    if ttInfos is None:
        print '这B号被封了'
        return '这B号被封了'
#    for  k, v in ttInfos.items():
#        print k, v
    print '总', ttInfos['Total']
    print '胜', ttInfos['Win']
    print '负', ttInfos['Lost']
    print 'R_Win', ttInfos['R_Win']
    print '天梯积分', rating
    print '排名', rank
#    print '排名前十', rankInfos
#    for k,v in ttInfos.items():
#        print k, ':', v
#    print '总场次:', ttInfos['Total']
#    print '胜率:', ttInfos['R_Win']
#    print '胜利:', ttInfos['Win']
#    print '失败:', ttInfos['Lost'] 
    print '逃跑率:', ttInfos['OfflineFormat']
#    
"YY.d.u = 347783110,YY.d.n = '二_十_五',YY.d.j = 333436659,YY.d.k = 'Turbogears' ,YY.wrt = '/',YY.page = 'rating';"
"YY.d.u = 333436659,YY.d.n = 'turbogears',YY.d.j = YY.d.u,YY.d.k = YY.d.n ,YY.wrt = '/',YY.page = 'rating';"
import re

get_ladder_score()
uid = get_uid_by_pname()
if uid!=None:
    get_rating(uid)
    get_hero_list(uid)
#计算最近100盘天梯加分-0分-扣分
#l = [2182, 2185, 2182, 2184, 2186, 2187, 2190, 2195, 2198, 2196, 2192, 2193, 2189, 2184, 2188, 2187, 2190, 2192, 2190, 2188, 2190, 2188, 2193, 2195, 2194, 2195, 2199, 2203, 2203, 2203, 2207, 2207, 2206, 2208, 2212, 2211, 2216, 2219, 2218, 2220, 2214, 2212, 2216, 2208, 2210, 2209, 2206, 2208, 2208, 2209, 2210, 2212, 2205, 2205, 2204, 2209, 2213, 2217, 2214, 2215, 2215, 2217, 2218, 2218, 2220, 2221, 2220, 2214, 2213, 2213, 2216, 2216, 2210, 2210, 2210, 2210, 2210, 2210, 2210, 2211, 2211, 2210, 2211, 2211, 2211, 2215, 2216, 2215, 2208, 2208, 2209, 2205, 2206, 2206, 2207, 2207, 2208, 2214, 2213, 2204]
#win = 0
#lost = 0
#draw = 0
#for i in range(0, len(l)-1):
#    if l[i]<l[i+1]:
#        win += 1
#    elif l[i]==l[i+1]:
#        draw += 1
#    else:
#        lost +=1
print 'end'#, lost, win, draw
#a = urllib.urlopen("http://www.baidu.com/img/shouye_b5486898c692066bd2cbaeda86d74448.gif")
#f = open('bd.gif', 'wb')
#f.write(a.read())




