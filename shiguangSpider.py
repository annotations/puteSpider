# -*- coding: utf-8 -*-
#---------------------------------------
#   程序：时光小屋爬虫
#   版本：0.1
#   作者：hhk
#   日期：2019-06-05
#   语言：Python 3.7
#   操作：时光小屋日益难用，把照片都爬下来放到NAS上
#---------------------------------------

import string
import time
import json
import jsonpath
import requests
import hashlib
import os

userId = "236742"
app_key = "6027a6b45d762a772b97779f078f2065"
cookie = "locale=zh-CN; Hm_lvt_abc9319e28ba129b86e23261fc67cb8d=1559706002; email=hhk0001%40gmail.com; phone=15651800896; user_session=BAhJIjpjbl8yMzY3NDJfOG9BNWxFUVMyR1pTZFlTLXZNMkV3WWZoMktnRmZKYmhTa1ZoOENXZzJqMAY6BkVU--e475fb77e0e0d657eac21e71548bc58c1e0f86a7; _saturn_session=ZHcvTDhZWVVqd3ppdE4xZGpKZjRVQ1p5QXVrOXNKQTZGYVZxTGNCWVVMdnFoL0UxRFoyQXlSeXZhSmRkVFZYMEYzNnNGekpQUElvYUZhMGRuc0w1S0ZJS2RxbllMMzd2azZNaGZZSklnSk54VU9JelNYRm1rdHJ5ZXBscnE5b0NYMTVKcWlKSXhtUDJ1Y08zejc3OEJBdHNMbWV4b2VobW5XUWRjTE1Pd3Vub2xxaDAvYkdwRGR1RGVIUGRlOXQwLS1WRVBZTzUrVkdmd09rSG1pRXcxMnF3PT0%3D--5197dfaf0339beda511a61a31e95bbbc9bb0dbcf; Hm_lpvt_abc9319e28ba129b86e23261fc67cb8d=1559706002"


def getPicList(id, formatTakenTime):
    # 图片保存目录
    picDircPath = "D:/imags/" + formatTakenTime
    param = "/events/" + str(id) + "?timestamp="
    url = signEventList(param)
    # url = "http://shiguangxiaowu.cn/events/"
    # postFix = "?timestamp=1559670109&sign=ccecace67eb08aba07a1e1e065907d1b"
    # 消息头直接从请求中爬的，还不知道哪几个是关键消息头
    headers = {#"Host": "shiguangxiaowu.cn",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
               "Accept": "application/json, text/javascript, */*; q=0.01",
               #"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
               #"Accept-Encoding": "gzip, deflate",
               "Referer": "http://shiguangxiaowu.cn/zh-CN/home/144185",
               #"X-NewRelic-ID": "VwIPUF9SGwAGVlBRDwk=",
               "X-Requested-With": "XMLHttpRequest",
               "Cookie": cookie
               }
    response = requests.get(url, headers=headers)
    #print(response.text)
    # 为空时打印并跳过
    if response.text.strip()=='':
        print("----")
        return
    dayEvent = json.loads(response.text)
    # 获取照片的URL
    picPathList = jsonpath.jsonpath(dayEvent, '$.moments[:].picture')

    # 判断目录是否存在,不存在创建目录
    if os.path.exists(picDircPath) == False:
        os.makedirs(picDircPath)
    # TODO 下载文件
    # TODO 增加入参，将文件按照日期保存至一个目录中
    # print(picPathList)
    count = 0
    if picPathList:
        for picPath in picPathList:
            response = requests.get(picPath, headers)
            # 获取的文本实际上是图片的二进制文本
            img = response.content
            # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
            localPicPath = picDircPath + "/" + str(count) + '.jpg'
            with open(localPicPath,'wb' ) as f:
                print(localPicPath)
                f.write(img)
                count += 1
    else:
        eventLog = " no photos under eventId : (%d) at %s" %(id, formatTakenTime)
        print(eventLog)


def signEventList(param):
    # 236742
    # 固定值
    timestamp = str(int(time.time()))
    # timestamp = "1559789167"
    param += timestamp
    m2 = hashlib.md5()   
    m2.update(param.encode('utf-8'))   
    paramSign = m2.hexdigest()
    # print(paramSign)
    ora_sign = userId + 'deny bad guy' + app_key + paramSign + ':::'
    # print(ora_sign)
    m3 = hashlib.md5() 
    m3.update(ora_sign.encode('utf-8'))
    sign = '&sign=' + m3.hexdigest()
    # print(sign)
    # http://shiguangxiaowu.cn/events.json?baby_id=144185&v=2&width=700&include_rt=true&timestamp=1559665693&sign=36e358459ec4d674647bde13a53b7b63
    url = "http://shiguangxiaowu.cn" + param + sign
    return url


def getEventList(next):
    param = "/events.json?baby_id=144185&v=2&width=700&include_rt=true&timestamp="
    url = signEventList(param)
    # 消息头直接从请求中爬的，目前确认的是，referer是必填的，否则查不到数据
    headers = {'cookie': cookie,
               #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0', 
               #"Accept": "application/json, text/javascript, */*; q=0.01",
               #"X-NewRelic-ID": "VwIPUF9SGwAGVlBRDwk=",
               "Referer": "http://shiguangxiaowu.cn/zh-CN/home/144185"
               }
    if next != -1 and next != None:
        url+="&before=" + str(next)
    # print(url)
    response = requests.get(url, headers=headers)
    print(response.text)
    
    # 为空时打印并跳过
    if response.text.strip()=='':
        print("====")
        return
    responseObj = json.loads(response.text)
    # 获取event列表。每个event对应一天
    eventList = jsonpath.jsonpath(responseObj, '$.list[:]')
    newNext = responseObj['next']
    print("new next: %d" %newNext)
    # 根据event获取当天的照片列表
    # TODO 获取列表中的"next",用于循环查询列表
    # getPicList(eventList[1]['id'],eventList[1]['months'], eventList[1]['days'], cookie)
    for event in eventList:
        eventId = event['id']
        months = event['months']
        days = event['days']
        takenGmt = event['taken_at_gmt']
        
        formatTakenTime = time.strftime("%Y%m%d", time.gmtime(takenGmt))
        #eventLog = "eventId : (%d). %dyear %dmonth %dday" %(eventId, months/12, months%12, days)
        #print(str)
        getPicList(eventId, formatTakenTime)
        time.sleep(20)
    return newNext


#-------- 输入参数 ------------------
#begin_date = input(u'请输入开始的日期（格式为%Y%m%d）：\n')
#end_date = input(u'请输入结束的日期（格式为%Y%m%d）：\n')
#-------- 输入参数 ------------------


#download_pute(begin_date,end_date)
next = getEventList(-1)
while next != -1:
        # 测试的时候发现联系请求会返回空数据,这里增加了一个等待时间
        time.sleep(30)
        next = getEventList(next)

# getPicList(697664092449596915, 99, 0)

# print (time.strftime("%Y%m%d", time.gmtime(1556899200)))

