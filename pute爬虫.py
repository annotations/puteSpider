# -*- coding: utf-8 -*-
#---------------------------------------
#   程序：普特听力爬虫
#   版本：0.1
#   作者：hhk
#   日期：2015-04-04
#   语言：Python 3.5
#   操作：输入需要下载的日期，将对应日期范围内的普特每日听力的内容下载下来。
#---------------------------------------
 
import string, datetime
from urllib.request import urlopen

filePaths = ("NPRNEWS","CNN","abcnews","voa","BBC")


#定义抓取函数
def download_pute(begin_date,end_date):
    begin_date_time = datetime.datetime.strptime(begin_date, "%Y%m%d")
    end_date_time = datetime.datetime.strptime(end_date, "%Y%m%d")
    timedelta = end_date_time - begin_date_time
    
    for i in range(timedelta.days + 1):
        curTimeDelta = datetime.timedelta(days=i)
        curDate = begin_date_time + curTimeDelta
        sCurMonth = curDate.strftime("%Y%m")
        sCurDay = curDate.strftime("%d")
        for file in filePaths:
            fileName = "putclub.com_" + sCurMonth + sCurDay + file + ".mp3"
            print ("正在下载" + fileName)
            f = open(fileName,'wb')
            response = urlopen("http://down02.putclub.com/virtual/backup/update/sest/" + sCurMonth + "/" + sCurDay + "/" + fileName)
            f.write(response.read())  
            f.close()  
            
 
 
#-------- 输入参数 ------------------
begin_date = input(u'请输入开始的日期（格式为%Y%m%d）：\n')
end_date = input(u'请输入结束的日期（格式为%Y%m%d）：\n')
#-------- 输入参数 ------------------
 

#
download_pute(begin_date,end_date)
