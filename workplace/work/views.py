# coding=utf8
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from django.db import models
from .models import Person
from .models import link
from .models import table
from .models import Persons
from .models import operate
from .models import process


import time
#from .models import weather
import sys  
from django.contrib import messages
man = ['se1','se2','se3']
IP=''
# Create your views here.
from django.http import HttpResponse

def login(request):         ##登录界面
    return render(request,'login.html')
 
def home(request):          ##主界面
    if 'user' in request.GET:       ##查表单键值 验证是否为第一次登陆
        person=Person.getPerson('user', request.GET['user'])
        if len(person)!=0 and person[0].password==request.GET['password']:
        #if Person.objects.get(user=request.GET['user']).user==request.GET['user'] and Person.objects.get(user=request.GET['user']).password==request.GET['password']:
#        if request.GET['user']=="zhangpc" and request.GET['password']=="21":
            request.session['user_id']=request.GET['user']
            #ip=weather.getIP(request)
            numofstatus=operate.numofstatus(request.session['user_id'],person[0].power)
            return render(request,'index.html',{'name':request.session['user_id'],'m':numofstatus,'power':person[0].power})
        else:
            messages.error(request,'错误的用户名或密码')
            return render(request,'login.html')
    else:                           #非第一次登陆
        person=Person.getPerson('user', request.session['user_id'])
        numofstatus=operate.numofstatus(request.session['user_id'],person[0].power)
        return render(request,'index.html',{'name':request.session['user_id'],'m':numofstatus,'power':person[0].power})
    
def success(request):       ##提交表单成功 转到主界面
    person=Person.getPerson('user', request.session['user_id'])
    if(request.GET['tatle']!='' and 'style' in request.session):
        pro=process.getProcess('styleid',request.session['style'])
        key=operate.cuttext(pro[0].message) 
        message=operate.gettext(key,request)
        table.createTable(request, person, message)
        del request.session['style']
    numofstatus=operate.numofstatus(request.session['user_id'],person[0].power)
    return render(request,'index.html',{'name':request.session['user_id'],'m':numofstatus,'power':person[0].power})

def new(request):           ##新建申请界面
    return render(request,'new.html',{'name': request.session['user_id']})

def change(request):        ##新建变更
    return render(request,'change.html',{'name': request.session['user_id']})

def myApple(request):       ##我申请的界面
    person=Person.getPerson('user', request.session['user_id'])
    tab=table.getTable('userid', person[0].id)
    return render(request,'myApple.html',{'name': request.session['user_id'],'tab':tab},)

def myAssignment(request):  ##分配给我的界面
    person=Person.getPerson('user', request.session['user_id'])
    lin=link.getLink('operid', person[0].id)
    if len(lin)!=0:
        tab=table.getTable('styleid', lin[0].styleid)
        return render(request,'myAssignment.html',{'name': request.session['user_id'],'tab':tab})
    return render(request,'myAssignment.html',{'name': request.session['user_id']})


def myOperated(request):    ##我操作过的界面
    person=Person.getPerson('user', request.session['user_id'])
    lin=link.getLink('operid', person[0].id)
    if len(lin)!=0:
        tab=table.getTable('styleid', lin[0].styleid)
        return render(request,'myOperated.html',{'name': request.session['user_id'],'tab':tab})
    return render(request,'myOperated.html',{'name': request.session['user_id']})

#def search(request):        ##提案搜索界面
#    return render(request,'search.html',{'name': request.session['user_id']})

def tablecontrol(request):  ##流程控制界面
    person=Person.getPerson('user',request.session['user_id'])
    if person[0].power !=2:       ##判断用户权限 不为2跳到error
        return render(request,'error.html',{'name': request.session['user_id']})
    else:
        lin=link.getLink('operid',person[0].id)
        pro=process.getProcess('styleid',lin[0].styleid)
        message=pro[0].message
        style=lin[0].typename
        return render(request,'tablecontrol.html',{'name': request.session['user_id'],'message':message,'style':style})   

def equipment(request):     ##提案统计界面
    person=Person.getPerson('user',request.session['user_id'])
    if person[0].power !=2: 
        return render(request,'error.html',{'name': request.session['user_id']})
    else:
        datacount=operate.getpie()
        return render(request,'equipment.html',{'name': request.session['user_id'],'d':datacount})

def detail(request):        ##提单详细查看界面
    tab=table.getTable('id', int(request.GET['id']))
    lin=link.getLink('styleid',tab[0].styleid)
    person=Person.getPerson('id', lin[0].operid)
    list=operate.cuttext(tab[0].content)
    key=operate.getdick(list[1],list[0])
    return render(request,'detail.html',{'list':list[1],'abc':key,'request':request,'table':tab[0],'link':lin[0], 'person':person[0]})
    
def result(request):        ##提单详细查看界面操作转主界面
    person=Person.getPerson('user', request.session['user_id'])
    numofstatus=operate.numofstatus(request.session['user_id'],person[0].power)
    if request.GET['key']=="1":
        table.getTable('id', request.GET['id']).update(result=1,status=3)
    elif request.GET['key']=="2":
        table.getTable('id', request.GET['id']).update(result=2,status=3)
    else:
        table.getTable('id', request.GET['id']).update(status=2)
    return render(request,'index.html',{'name':request.session['user_id'],'m':numofstatus,'power':person[0].power})

def create(request):            ##创建提案界面
    request.session['style'] = int(request.GET['style'])
    sty=link.getLink('styleid',int(request.GET['style']))
    pro=process.getProcess("styleid",int(request.GET['style']))
    typename=sty[0].typename
    key=operate.cuttext(pro[0].message)
    return render(request,'create.html',{'name': request.session['user_id'],'abc':key,'typename':typename})        #{'name':a[0]})#,{'style':style})

def logout(request):            ##登出界面
    del request.session['user_id']
    return render(request,'login.html')

@csrf_exempt    
def welcome(request):
    #q=''
    #for n in man:
    #    q=q+request.POST[n]+'#'
    #key=operate.cuttext(q)
    #d={[]}
    #m=['IEee','eeee']
    #if len(Person.getPerson('user','xuys'))==0 :
    #   m=Person.getPerson('user','zhangpc')[0]
    request.session['test']='user' 
    return render(request,'welcome.html',{'m':request})


def test(request):
    pro=process.getProcess("styleid",3)
    key=operate.cuttext(pro[0].message)
    return render(request,'test.html',{'abc':key})        #{'name':a[0]})#,{'style':style})

def tese(request):
    json=request.GET['lalala']
    return render(request,'test2.html',{{'a':json}})


def tablesuccess(request):      ##流程控制界面修改成功跳转到开始界面
    if operate.checktest(request.GET['message'])==1:
        person=Person.getPerson('user', request.session['user_id'])
        lin=link.getLink('operid', person[0].id)
        process.getProcess('styleid',lin[0].styleid).update(message=request.GET['message'])
    person=Person.getPerson('user', request.session['user_id'])
    numofstatus=operate.numofstatus(request.session['user_id'],person[0].power)
    return render(request,'index.html',{'name':request.session['user_id'],'m':numofstatus,'power':person[0].power})

def pagenofound(request):
    return render(request,'error404.html')

def pageerror(request):
    return render(request,'error500.html')
