#coding:utf8
from __future__ import print_function
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import simplejson
 
import os
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
 
try:
    import urllib2 as wdf_urllib
    from cookielib import CookieJar
except ImportError:
    import urllib.request as wdf_urllib
    from http.cookiejar import CookieJar
 
import re
import time
import xml.dom.minidom
import json
import sys
import math
import subprocess
import ssl
import urllib
import urllib2
import cookielib
import memcache
#import pylibmc as memcache
# Create your views here.

DEBUG = False
#DEBUG = True
 
MAX_GROUP_NUM = 35 
INTERFACE_CALLING_INTERVAL = 16
MAX_PROGRESS_LEN = 50
deviceId = 'e000000000000000'
 
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

postdata = {
    'a' : '1'
}
try:
    xrange
    range = xrange
except:
    # python 3
    pass
 
def getRequest(url, data=None):
    try:
        data = data.encode('utf-8')
    except:
        pass
    finally:
        return wdf_urllib.Request(url=url, data=data)
 
def getUUID():
 
    url = 'https://login.weixin.qq.com/jslogin'
    params = {
        'appid': 'wx782c26e4c19acffb',
        'fun': 'new',
        'lang': 'zh_CN',
        '_': int(time.time()),
    }
 
    request = getRequest(url=url, data=urlencode(params))
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
    # print(data)
 
    regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
    pm = re.search(regx, data)
 
    code = pm.group(1)
    uuid = pm.group(2)
 
    return uuid
 
 
def waitForLogin(uuid):
    base_uri = ''
    redirect_uri = ''
    tip = 0 
    url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s' % (
        tip, uuid, int(time.time()))
 
    request = getRequest(url=url)
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
    regx = r'window.code=(\d+);'
    pm = re.search(regx, data)
 
    code = pm.group(1)
 
    if code == '201':
        tip = 0
    elif code == '200':
        regx = r'window.redirect_uri="(\S+?)";'
        pm = re.search(regx, data)
        redirect_uri = pm.group(1) + '&fun=new'
        base_uri = redirect_uri[:redirect_uri.rfind('/')]
 
    elif code == '408':
        pass
    waitlogin_dict = {'tip': tip, 'base_uri': base_uri, 'redirect_uri': redirect_uri, 'code': code}
    #print("tip:%d\nbase_uri:%s\nredirect_uri:%s"%(tip, base_uri, redirect_uri)) 
    return waitlogin_dict
 
def login(redirect_uri):
 
    request = getRequest(url=redirect_uri)
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
 
    '''
        <error>
            <ret>0</ret>
            <message>OK</message>
            <skey>xxx</skey>
            <wxsid>xxx</wxsid>
            <wxuin>xxx</wxuin>
            <pass_ticket>xxx</pass_ticket>
            <isgrayscale>1</isgrayscale>
        </error>
    '''
 
    doc = xml.dom.minidom.parseString(data)
    root = doc.documentElement
 
    for node in root.childNodes:
        if node.nodeName == 'skey':
            skey = node.childNodes[0].data
        elif node.nodeName == 'wxsid':
            wxsid = node.childNodes[0].data
        elif node.nodeName == 'wxuin':
            wxuin = node.childNodes[0].data
        elif node.nodeName == 'pass_ticket':
            pass_ticket = node.childNodes[0].data
 
    # print('skey: %s, wxsid: %s, wxuin: %s, pass_ticket: %s' % (skey, wxsid,
    # wxuin, pass_ticket))
 
 
    BaseRequest = {
        'Uin': int(wxuin),
        'Sid': wxsid,
        'Skey': skey,
        'DeviceID': deviceId,
    }
    logindict = {'skey': skey, 'wxsid': wxsid, 'wxuin': wxuin, 'pass_ticket': pass_ticket, 'BaseRequest': BaseRequest} 
    #print("skye:%s\nwxsid:%s\nwxuin:%s\npass_ticket:%s\nBaseRequest:%s"%(skey, wxsid, wxuin, pass_ticket, BaseRequest))
    return logindict
 
def webwxinit(base_uri, BaseRequest, pass_ticket, skey):
 
    url = base_uri + \
        '/webwxinit?pass_ticket=%s&skey=%s&r=%s' % (
            pass_ticket, skey, int(time.time()))
    params = {
        'BaseRequest': BaseRequest
    }
 
    request = getRequest(url=url, data=json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read()
 
    if DEBUG:
        f = open(os.path.join(os.getcwd(), 'webwxinit.json'), 'wb')
        f.write(data)
        f.close()
 
    data = data.decode('utf-8', 'replace')
 
    # print(data)
 
    dic = json.loads(data)
    ContactList = dic['ContactList']
    My = dic['User']
 
    SyncKeyList = []
    for item in dic['SyncKey']['List']:
        SyncKeyList.append('%s_%s' % (item['Key'], item['Val']))
    SyncKey = '|'.join(SyncKeyList)
 
    ErrMsg = dic['BaseResponse']['ErrMsg']
    if DEBUG:
        print("Ret: %d, ErrMsg: %s" % (dic['BaseResponse']['Ret'], ErrMsg))
 
    Ret = dic['BaseResponse']['Ret']
    if Ret != 0:
        return False
    webwxinitdict = {'ContactList': ContactList, 'My': My, 'SyncKey': SyncKey}
    #print("ContactList:%s\nMy:%s\nSyncKey:%s"%(ContactList, My, SyncKey))
    return webwxinitdict
 
def webwxgetcontact(base_uri, pass_ticket, skey, My):
 
    url = base_uri + \
        '/webwxgetcontact?skey=%s&r=%s' % (
            skey, int(time.time()))
    data = urllib2.urlopen(url).read()
    if DEBUG:
        f = open(os.path.join(os.getcwd(), 'webwxgetcontact.json'), 'wb')
        f.write(data)
        f.close()
 
    #print(data)
    data = data.decode('utf-8', 'replace')
 
    dic = json.loads(data)
    MemberList = dic['MemberList']
 
    SpecialUsers = ["newsapp", "fmessage", "filehelper", "weibo", "qqmail", "tmessage", "qmessage", "qqsync", "floatbottle", "lbsapp", "shakeapp", "medianote", "qqfriend", "readerapp", "blogapp", "facebookapp", "masssendapp",
                    "meishiapp", "feedsapp", "voip", "blogappweixin", "weixin", "brandsessionholder", "weixinreminder", "wxid_novlwrv3lqwv11", "gh_22b87fa7cb3c", "officialaccounts", "notification_messages", "wxitil", "userexperience_alarm"]
    for i in range(len(MemberList) - 1, -1, -1):
        Member = MemberList[i]
        if Member['VerifyFlag'] & 8 != 0:
            MemberList.remove(Member)
        elif Member['UserName'] in SpecialUsers:
            MemberList.remove(Member)
        elif Member['UserName'].find('@@') != -1:
            MemberList.remove(Member)
        elif Member['UserName'] == My['UserName']:
            MemberList.remove(Member)
 
    return MemberList
 
def createChatroom(UserNames, pass_ticket, base_uri, BaseRequest):
    MemberList = [{'UserName': UserName} for UserName in UserNames]
 
    url = base_uri + \
        '/webwxcreatechatroom?pass_ticket=%s&r=%s' % (
            pass_ticket, int(time.time()))
    params = {
        'BaseRequest': BaseRequest,
        'MemberCount': len(MemberList),
        'MemberList': MemberList,
        'Topic': '',
    }
 
    request = getRequest(url=url, data=json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
    # print(data)
 
    dic = json.loads(data)
    ChatRoomName = dic['ChatRoomName']
    MemberList = dic['MemberList']
    DeletedList = []
    for Member in MemberList:
        if Member['MemberStatus'] == 4:
            DeletedList.append(Member['UserName'])
 
    ErrMsg = dic['BaseResponse']['ErrMsg']
    if DEBUG:
        print("Ret: %d, ErrMsg: %s" % (dic['BaseResponse']['Ret'], ErrMsg))
 
    return ChatRoomName, DeletedList
 
def deleteMember(ChatRoomName, UserNames, pass_ticket, base_uri, BaseRequest):
    url = base_uri + \
        '/webwxupdatechatroom?fun=delmember&pass_ticket=%s' % (pass_ticket)
    params = {
        'BaseRequest': BaseRequest,
        'ChatRoomName': ChatRoomName,
        'DelMemberList': ','.join(UserNames),
    }
 
    request = getRequest(url=url, data=json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
    # print(data)
 
    dic = json.loads(data)
    ErrMsg = dic['BaseResponse']['ErrMsg']
    Ret = dic['BaseResponse']['Ret']
    if DEBUG:
        print("Ret: %d, ErrMsg: %s" % (Ret, ErrMsg))
 
    if Ret != 0:
        return False
 
    return True
 
def addMember(ChatRoomName, UserNames, pass_ticket, base_uri, BaseRequest):
    url = base_uri + \
        '/webwxupdatechatroom?fun=addmember&pass_ticket=%s' % (pass_ticket)
    params = {
        'BaseRequest': BaseRequest,
        'ChatRoomName': ChatRoomName,
        'AddMemberList': ','.join(UserNames),
    }
 
    request = getRequest(url=url, data=json.dumps(params))
    request.add_header('ContentType', 'application/json; charset=UTF-8')
    response = wdf_urllib.urlopen(request)
    data = response.read().decode('utf-8', 'replace')
 
    # print(data)
 
    dic = json.loads(data)
    MemberList = dic['MemberList']
    DeletedList = []
    for Member in MemberList:
        if Member['MemberStatus'] == 4:
            DeletedList.append(Member['UserName'])
 
    ErrMsg = dic['BaseResponse']['ErrMsg']
    if DEBUG:
        print("Ret: %d, ErrMsg: %s" % (dic['BaseResponse']['Ret'], ErrMsg))
 
    return DeletedList
 

def index(request):
    if request.method == "GET":
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
 
            opener = wdf_urllib.build_opener(
                wdf_urllib.HTTPCookieProcessor(CookieJar()))
            wdf_urllib.install_opener(opener)
        except:
            pass
        uuid = getUUID()
        url = 'https://login.weixin.qq.com/qrcode/' + uuid
        params = {
            't': 'webwx',
            '_': int(time.time()),
        }
 
        request = getRequest(url=url, data=urlencode(params))
        response = wdf_urllib.urlopen(request)
        context = {
            'uuid': uuid,
            'response': response.read(),
            'delyou': '',
            }
        return render_to_response('index.html', context)
    
def checkwx(request):
    if request.method == "GET":
        uuid = str(request.GET.get('uuid'))
        mc = memcache.Client(['127.0.0.1:11211'])
        mccontext = mc.get(uuid)
        base_uri, redirect_uri, BaseRequest, pass_ticket, skey, ContactList, My, SyncKey = mccontext['base_uri'], mccontext['redirect_uri'],\
          mccontext['BaseRequest'], mccontext['pass_ticket'], mccontext['skey'], mccontext['ContactList'], mccontext['My'], mccontext['SyncKey']

        MemberList = webwxgetcontact(base_uri, pass_ticket, skey, My)
        #print(MemberList)
 
        MemberCount = len(MemberList)
        print('通讯录共%s位好友' % MemberCount)
 
        ChatRoomName = ''
        result = []
        d = {}
        for Member in MemberList:
            d[Member['UserName']] = (Member['NickName'].encode(
                'utf-8'), Member['RemarkName'].encode('utf-8'))
        print('开始查找...')
        group_num = int(math.ceil(MemberCount / float(MAX_GROUP_NUM)))
        for i in range(0, group_num):
            UserNames = []
            for j in range(0, MAX_GROUP_NUM):
                if i * MAX_GROUP_NUM + j >= MemberCount:
                    break
                Member = MemberList[i * MAX_GROUP_NUM + j]
                UserNames.append(Member['UserName'])

            # 新建群组/添加成员 
            if ChatRoomName == '':
                (ChatRoomName, DeletedList) = createChatroom(UserNames, pass_ticket, base_uri, BaseRequest)
            else:
                DeletedList = addMember(ChatRoomName, UserNames, pass_ticket, base_uri, BaseRequest)
 
            DeletedCount = len(DeletedList)
            if DeletedCount > 0:
                result += DeletedList
 
            # 删除成员
            deleteMember(ChatRoomName, UserNames, pass_ticket, base_uri, BaseRequest)
 
            # 进度条
            progress_len = MAX_PROGRESS_LEN
            progress = '-' * progress_len
            progress_str = '%s' % ''.join(
                map(lambda x: '#', progress[:(progress_len * (i + 1)) / group_num]))
            print(''.join(
                ['[', progress_str, ''.join('-' * (progress_len - len(progress_str))), ']']))
            print('新发现你被%d人删除' % DeletedCount)
            for i in range(DeletedCount):
                if d[DeletedList[i]][1] != '':
                    print(d[DeletedList[i]][0] + '(%s)' % d[DeletedList[i]][1])
                else:
                    print(d[DeletedList[i]][0])
 
            if i != group_num - 1:
                print('正在继续查找,请耐心等待......')
                # 下一次进行接口调用需要等待的时间
                time.sleep(INTERFACE_CALLING_INTERVAL)
 
        # todo 删除群组
        print('\n结果汇总完毕,20s后可重试...')
        resultNames = []
        for r in result:
            if d[r][1] != '':
                resultNames.append(d[r][0] + '(%s)' % d[r][1])
            else:
                resultNames.append(d[r][0])
 
        print('---------- 被删除的好友列表(共%d人) ----------' % len(result))
        # 过滤emoji
        resultNames = map(lambda x: re.sub(r'<span.+/span>', '', x), resultNames)
        if len(resultNames):
            print('\n'.join(resultNames))
            delyou = 'and'.join(resultNames) + ' 把你给删除了!'
        else:
            print("无")
            delyou = '你好牛叉啊，没有人敢删你!'
        print('---------------------------------------------')
        context = {
            'uuid': uuid,
            'delyou': delyou,
           }
        return render_to_response('checkwx.html', context)



def check(request):
    ContactList = []
    My = []
    SyncKey = ''
    BaseRequest = {}
    if request.method == "GET":
        uuid = str(request.GET.get('uuid', ''))
        #print(uuid)
        #获取登陆
        waitforlogin = waitForLogin(uuid)
        #print(waitforlogin['code'])
        #如果已经扫描点登陆返回key为200
	if waitforlogin['code'] == '200':
            #print('jing ru')
            base_uri, redirect_uri = waitforlogin['base_uri'], waitforlogin['redirect_uri']
            #print('2 jing')
            #print(redirect_uri)
            #print(base_uri)
            #正式登陆，重要获取 skey  wxsid wxuid
            logindict = login(redirect_uri)
            #print('3 jing')
            BaseRequest, pass_ticket, skey = logindict['BaseRequest'], logindict['pass_ticket'], logindict['skey']
            #print(logindict)
            #初始化，获取ContactList, My, SyncKey
            webwxinitdict = webwxinit(base_uri, BaseRequest, pass_ticket, skey)
            #print(webwxinitdict)
            ContactList, My, SyncKey = webwxinitdict['ContactList'], webwxinitdict['My'], webwxinitdict['SyncKey']
            #ajax返回以上值，也可以服务端存储到redis或者Memcached
            mccontext = {
               'uuid': uuid,
               'base_uri': base_uri,
               'redirect_uri': redirect_uri,
               'BaseRequest': BaseRequest,
               'pass_ticket': pass_ticket,
               'skey': skey,
               'ContactList': ContactList,
               'My': My,
               'SyncKey': SyncKey
               }
            mc = memcache.Client(['127.0.0.1:11211'])
            mc.set(uuid, mccontext)
            context = {
               'uuid': uuid,
               'return_code': 'done',
               }
        else:
            context = {
               'uuid': uuid,
               'return_code': 'fall',
               }
        return HttpResponse(simplejson.dumps(context, ensure_ascii=False))
