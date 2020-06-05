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
cookie = "locale=zh-CN; user_session=BAhJIjpjbl8yMzY3NDJfTURoT0ZQLUFkdGFlaTNTc1p3VkQwdGFnTkZRRVp3RU91RzJlbWg1TE1qVQY6BkVU--222591fbd9634241ad259d088e510e786dd889e6"
eventFile = open("eventList.txt","a")

def getPicList(id, formatTakenTime):
    # 图片保存目录
    picDircPath = "D:/imags2/" + formatTakenTime
    param = "/events/" + str(id) + "?timestamp="
    # url = signEventList(param)
    
    eventFile.write(str(id))
    eventFile.write(",")
    eventFile.write(formatTakenTime)
    eventFile.write("\n")

def getPicFromEvent(event, formatTakenTime):
    # 图片保存目录
    picDircPath = "D:/imags2/" + formatTakenTime

    # 获取layout_detail列表。对应图片详情列表
    detailList = event['layout_detail']

    if detailList:
        if os.path.exists(picDircPath) == False:
            os.makedirs(picDircPath)
        for detail in detailList:
            if (detail['type'] != 'picture'):
                continue
            picture = detail['picture']
            id = detail['id']
            response = requests.get(picture)
            # 获取的文本实际上是图片的二进制文本
            img = response.content
            # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
            localPicPath = picDircPath + "/" + str(id) + '.jpg'
            with open(localPicPath,'wb' ) as f:
                print(localPicPath)
                f.write(img)
            time.sleep(5)
    # param = "/events/" + str(id) + "?timestamp="
    # # url = signEventList(param)
    
    # eventFile.write(str(id))
    # eventFile.write(",")
    # eventFile.write(formatTakenTime)
    # eventFile.write("\n")

def getPicFromUrl(url, id, picDircPath):
    # 消息头直接从请求中爬的，还不知道哪几个是关键消息头
    headers = {
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
               "Accept": "application/json, text/javascript, */*; q=0.01",
               "Referer": "http://shiguangxiaowu.cn/zh-CN/home/144185",
               "X-Requested-With": "XMLHttpRequest",
               "Cookie": cookie
               }
    response = requests.get(url, headers=headers)
    # print(response.text)
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
        time.sleep(5)
    else:
        eventLog = " no photos under eventId : (%d) at %s" %(id, picDircPath)
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
    url = "http://www.shiguangxiaowu.cn" + param + sign
    return url


def getEventList(next):
    param = "/events?baby_id=144185&style=best_12&include_rt=true"
    # 消息头直接从请求中爬的，目前确认的是，referer是必填的，否则查不到数据
    headers = {'cookie': cookie,
               "Referer": "http://shiguangxiaowu.cn/zh-CN/home/144185"
               }
    if next != -1 and next != None:
        param+="&before=" + str(next)
    # print(url)
    param+="&timestamp="
    url = signEventList(param)
    print(url)
    response = requests.get(url, headers=headers)
    print(response.text)
    
    # 为空时打印并跳过
    if response.text.strip()=='':
        print("==empty event list==")
        return
    responseObj = json.loads(response.text)
    # 获取event列表。每个event对应一天
    eventList = jsonpath.jsonpath(responseObj, '$.list[:]')
    newNext = responseObj['next']
    if newNext:
        print("new next: %d" %newNext)

    # 根据event获取当天的照片列表
    # TODO 获取列表中的"next",用于循环查询列表
    # getPicList(eventList[1]['id'],eventList[1]['months'], eventList[1]['days'], cookie)
    for event in eventList:
        # eventId = event['id']
        # months = event['months']
        # days = event['days']
        takenGmt = event['taken_at_gmt']
        
        formatTakenTime = time.strftime("%Y%m%d", time.gmtime(takenGmt))
        #eventLog = "eventId : (%d). %dyear %dmonth %dday" %(eventId, months/12, months%12, days)
        #print(str)
        getPicFromEvent(event, formatTakenTime)
        # time.sleep(20)
    return newNext


#-------- 输入参数 ------------------
#begin_date = input(u'请输入开始的日期（格式为%Y%m%d）：\n')
#end_date = input(u'请输入结束的日期（格式为%Y%m%d）：\n')
#-------- 输入参数 ------------------


#download_pute(begin_date,end_date)
next = getEventList(19)
while next:
        # 测试的时候发现连续请求会返回空数据,这里增加了一个等待时间
        time.sleep(30)
        next = getEventList(next)

# getPicList(697664092449596915, 99, 0)

# print (time.strftime("%Y%m%d", time.gmtime(1556899200)))

# getPicFromUrl("http://www.shiguangxiaowu.cn/events/724053440988243867?timestamp=1564458227&sign=da1ab0c7d8fb1a560e3045151790b7b5",
# 719123883336197938, "D:/imags2/2")

eventFile.close()