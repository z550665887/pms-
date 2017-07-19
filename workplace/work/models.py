
from django.db import models
from django.core.management.color import Style
from django.http import HttpResponse
from collections import OrderedDict
from django.db.models import Q
import matplotlib.pyplot as plt
import time
import random
import smtplib
from email.mime.text import MIMEText
from email import encoders
# Create your models here.

class Person(models.Model):
    user=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    telephone=models.CharField(max_length=30)
    power=models.IntegerField()
    def __str__(self):
    # 在Python3中使用 def __str__(self)
        return self.user
    def getPerson(str1,str2):  # @NoSelf
        if str1=='user':
            return Person.objects.filter(user=str2)
        elif str1=='id':
            return Person.objects.filter(id=str2)
        
class table(models.Model):
    styleid=models.IntegerField()
    type = models.CharField(max_length=30)
    critical=models.IntegerField()
    userid=models.IntegerField()
    status=models.IntegerField()
    content=models.CharField(max_length = 500)
    result=models.IntegerField()
    user=models.CharField(max_length=30)
    def getTable(str1,str2):  # @NoSelf
        if str1=='styleid':
            return table.objects.filter(styleid=str2)
        elif str1=='userid':
            return table.objects.filter(userid=str2)  
        elif str1=='id':
            return table.objects.filter(id=str2)  
        
    def createTable(request,person,message):  # @NoSelf
        table.objects.create(styleid=request.session['style'],
                             type=request.GET['tatle'],userid=person[0].id,user=person[0].user,critical=1,status=1,content=message,result=0) 
        
class  link(models.Model):
    operid=models.IntegerField()
    styleid=models.IntegerField()
    typename=models.CharField(max_length=30)
    def getLink(str1,str2):  # @NoSelf
        if str1=='styleid':
            return link.objects.filter(styleid=str2)
        elif str1=='operid':
            return link.objects.filter(operid=str2)   
        

class Persons(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    message = models.TextField()
    

class process(models.Model):
    message=models.TextField()
    styleid=models.IntegerField()
    def getProcess(str1,str2):  # @NoSelf
        if str1=='id':
            return process.objects.filter(id=str2)
        elif str1=='styleid':
            return process.objects.filter(styleid=str2)
        

class operate(models.Model):
    def cuttext(str1):              ###将指定格式的text文本切成列表 返回列表 @NoSelf
        key=[]
        key1=[]
        p=''
        stmp=0
        for n in str1:
            if n=='#'and stmp==0:
                key.append(p)
                p=''
            elif n!='#'and stmp==0:
                p=p+n
            if n=='@':
                p=''
                stmp=1
            elif n=='#'and stmp==1:
                key1.append(p)
                p=''
            elif n!='#'and stmp==1:
                p=p+n     
        if stmp==1:
            return key,key1
        else:
            return key
        
    def gettext(list1,request):     ###根据列表作为键值 取出对应request的值 并将其拼成指定格式的text 返回text @NoSelf
        key=''
        for n in list1:
            key=key+request.GET[n]+'#'
        key=key+'@'
        for n in list1:
            key=key+n+'#'
        return key
    
    def getdick(list1,list2):       ###将流程作为KEY 将内容作为value 返回dict @NoSelf
        d=OrderedDict()
        for n in range(len(list1)):
            d[list1[n]]=list2[n]
        return d
    
    def numofstatus(a,power):       ###登录用户的提案数量塞选功能 @NoSelf
        m=[]
        if power==2:
            m.append(len(table.objects.filter(Q(styleid=link.objects.filter(operid=Person.objects.get(user=a).id)[0].styleid),Q(status=1))))
            m.append(len(table.objects.filter(Q(styleid=link.objects.filter(operid=Person.objects.get(user=a).id)[0].styleid),Q(result=0)))-m[0])
        else:
            m.append(0)
            m.append(0)
        m.append(len(table.objects.filter(Q(userid=Person.objects.get(user=a).id),Q(status=1))))
        m.append(len(table.objects.filter(Q(userid=Person.objects.get(user=a).id),Q(result=0)))-m[2])
        return m
    
    def checktest(text):            ###流程控制的修改检查 @NoSelf
        if text[len(text)-1]!='#' or text[0]=='#':
            return 0
        for i in range(len(text)-1):
            if text[i]=='#'and text[i+1]=='#'and i != len(text):
                return 0
        return 1
    
    def getpie():  # @NoSelf
        #plt.rcParams['font.sans-serif']=['SimHei']
        #plt.rcParams['axes.unicode_minus']=False
        #plt.figure(figsize=(4,3))       ###以上代码为画图初始化设置
        d=OrderedDict()
        m=len(table.objects.all())
        for a in link.objects.all():
            d[a.typename]=[len(table.objects.filter(styleid=a.styleid))/m,'#'+hex(int(random.uniform(0.5,1)*16777215)).replace('0x','',1)]
        return d
        #plt.pie(size,labels=labels,autopct='%1.1f%%',shadow=True,startangle=90) #画图函数
        #plt.axis('equal') #让保持圆形 
        #plt.savefig('workplace/workplace/work/static/pltimg/'+str+'.png')              #workplace/workplace/work/
        #time.sleep(1)
        #plt.close('all')
        #return '/static/pltimg/'+str+'.png'
        
    def sendmail2(to,body,subject):  # @NoSelf
        MAIL_HOST = "smtp.126.com"
        MAIL_USER = "z550665887"
        MAIL_FROM = "z550665887@126.com"
        MAIL_PWD = "zpc159357"
        msg = MIMEText(body,"html","utf-8")
        msg['From'] = MAIL_FROM
        msg['Subject'] = subject
        msg['To'] = str
        smtp = smtplib.SMTP()
        smtp.connect(MAIL_HOST,25)
        smtp.login(MAIL_USER, MAIL_PWD)
        smtp.sendmail(MAIL_FROM, '447143800@qq.com', msg.as_string())
        smtp.quit()
#class weather(models.Model):
 #   def getIP(requert):
 #       return request.META['REMOTE_ADDR']
        
 #   def getcity(request):
 #       ip=request.META['REMOTE_ADDR']
 #       URL = 'http://freeipapi.17mon.cn/' + ip
 #       try:
 #           r = requests.get(URL, timeout=3)
#        except requests.RequestException as e:
 #           print(e)
 #       json_data = r.json()
 #       return json_data[2]
        