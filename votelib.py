#!/usr/bin/env python3
# coding=utf-8

from urllib import request, parse
import http.cookiejar as cookielib
import os
import json
import logging

class VoteHelper(object):
    """docstring for   HttpHelper"""
    def __init__(self):
        self.has_login = False

    def __do_login(self,name,pwd):
        result = False
        cookie_jar2 = cookielib.LWPCookieJar()
        cookie_support2 = request.HTTPCookieProcessor(cookie_jar2)
        opener2 = request.build_opener(cookie_support2, request.HTTPHandler)
        request.install_opener(opener2)

        req = request.Request('http://gench.yiban.cn/login.php')
        req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
        req.add_header('Referer', 'http://gench.yiban.cn')

        login_data = parse.urlencode([
            ('username', name),
            ('passwd', pwd)
        ])
        with request.urlopen(req,data=login_data.encode('utf-8')) as f:
            back_html =    str( f.read(), encoding="utf-8")
            if back_html == '<script>location.href="/";</script>':
                result=True
        return result

    def vote(self,username,passwd,app_id=10675,vote_id=115,vote_option_id=773):

        self.__do_login(username,passwd)

        req = request.Request('http://q.yiban.cn/vote/insertBoxAjax')
        vote_data = parse.urlencode([
            ('App_id',app_id),
            ('Vote_id',vote_id),
            ('VoteOption_id',vote_option_id)
        ])
        with request.urlopen(req,data=vote_data.encode('utf-8')) as f:
            result = f.read().decode('utf-8')
            try:
                json_data = json.loads(result)
                if(json_data['code']==200):
                    print('投票成功！用户名：%s' % username)
                    return 200
                elif(json_data['code']==206):
                    print('投票失败(重复投票)！用户名：%s' % username)
                    return 206
                elif(json_data['code']==211):
                    print('投票失败(登录问题)!用户名：%s' % username)
                    return 211
                elif(json_data['code']==204):
                    print('投票失败(投票上线)!用户名：%s' % username)
                    return 204
            except Exception:
                print('投票失败(返回不为json)！用户名：%s' % username)
            # print(json.dumps(json_data))
            # print('vote result:'+str(json_data['code']))
        return 0

    def addcomment(self,username,passwd,appid=166525,type='extendcomment',code='extendcomment-1510073493139',title='说出你想对这些清云奖候选人想说的话',content="QQ群372875758",isAnonymous=1,isFeed=2,App_id=166525,url='https://q.yiban.cn/comment/addComment'):
        result =""
        if self.__do_login(username, passwd):
            req = request.Request(url)
            vote_data = parse.urlencode([
                ('appid', appid),
                ('type', type),
                ('code', code),
                ('title', title),
                ('content', content),
                ('isAnonymous', isAnonymous),
                ('isFeed', isFeed),
                ('App_id', App_id)
            ])
            with request.urlopen(req, data=vote_data.encode('utf-8')) as f:
                result = f.read().decode('utf-8')
        return result