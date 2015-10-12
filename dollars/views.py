__author__ = 'triThirty'

from django.shortcuts import *
from django.template.context_processors import *
from django.http import *
import datetime
from dollars import myMongo
from dollars import getMD5
import arrow
import redis


rds0 = redis.StrictRedis()
mm=myMongo.myMongo()
def homepage(request):
    c = {}
    c.update(csrf(request))
    # if request.method=='POST' and request.POST['password']!='':
    #     password=request.POST['password']
    #     print('this is password:'+password)
    #     result = mm.find_one({'password':password})
    #     if result!=None:
    #         return HttpResponseRedirect('/chatroom')
    #     else:
    #          return HttpResponseRedirect('/')
    if request.method=='GET':
        print('GET')
        print(request.path)
        return render_to_response('dollars/homepage.html',c)
    else:
        print('error')
        return HttpResponseRedirect('/')

def chatroom(request):
    if request.method=='POST' and request.POST['password']!='':
        password=request.POST['password']
        result = mm.find_one({'password':password})
        if result!=None:
            response=render_to_response('dollars/chatroom.html',)
            m = getMD5.MD5()
            try:
                request.META['HTTP_X_FORWARDED_FOR']
                ip = request.META['HTTP_X_FORWARDED_FOR']
            except:
                ip = request.META['REMOTE_ADDR']
            print(ip)
            s = ip + str(arrow.utcnow().to('Asia/Shanghai'))
            mm1 = m.getMD5(s.encode())
            print(mm1.hexdigest())
            v=mm1.hexdigest()
            response.set_cookie("uid",value=v)
            rds0.hmset(v,{"nick_name":result["nickname"],"avatar":result["img"]})
            return response
        else:
             return HttpResponseRedirect('http://localhost')
    else:
        return HttpResponseRedirect('http://localhost')





# def loginrequst(url):
#     def decoretor(fnc):
#         def wrapper(*args, **kw):
#             v=request.cookie["uid"]
#             if(v):
#                 if(rds0.hmget(v,("avatar","nick_name"))):
#                     return fnc(*args, **kw)
#             else:redirect(url)
#             return fnc(*args, **kw)
#         return wrapper
#     return decoretor