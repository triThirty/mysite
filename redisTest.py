import threading, time, httplib2
HOST = "http://www.baidu.com"; #主机地址 例如192.168.1.101
PORT = 80 #端口  
URI = "/?123" #相对地址,加参数防止缓存，否则可能会返回304  
TOTAL = 0 #总数  
SUCC = 0 #响应成功数  
FAIL = 0 #响应失败数  
EXCEPT = 0 #响应异常数  
MAXTIME=0 #最大响应时间  
MINTIME=100 #最小响应时间，初始值为100秒  
GT3=0 #统计3秒内响应的  
LT3=0 #统计大于3秒响应的  
# 创建一个 threading.Thread 的派生类  
class RequestThread(threading.Thread):  
    # 构造函数  
    def __init__(self, thread_name):  
        threading.Thread.__init__(self)  
        self.test_count = 0  
  
    # 线程运行的入口函数  
    def run(self):
        self.test_performace()  
  
  
    def test_performace(self):  
            global TOTAL  
            global SUCC  
            global FAIL  
            global EXCEPT  
            global GT3  
            global LT3  
            try:  
                i=0
                while i<=200:
                    st = time.time()
                    h = httplib2.Http(".cache")
                    res, content = h.request(HOST)
                    if res.status == 200:
                        TOTAL+=1
                        SUCC+=1
                    else:
                        TOTAL+=1
                        FAIL+=1
                    time_span = time.time()-st
                    # print('%s:%f\n'%(self.name,time_span))
                    self.maxtime(time_span)
                    self.mintime(time_span)
                    if time_span>3:
                        GT3+=1
                    else:
                        LT3+=1
                    i=i+1
                print(self.name+":end")
                callBack(self.name)
            except Exception as e:
                print(e)
                TOTAL+=1  
                EXCEPT+=1
    def maxtime(self,ts):  
            global MAXTIME  
            # print(ts)
            if ts>MAXTIME:  
                MAXTIME=ts  
    def mintime(self,ts):  
            global MINTIME  
            if ts<MINTIME:  
                MINTIME=ts  
          
# main 代码开始  
print('===========task start===========')
# 并发的线程数  
thread_count =5
  
i = 1
while i <=thread_count:
    t = RequestThread("thread" + str(i))  
    t.start()
    print("thread" + str(i)+":start")
    i += 1  
t=0  
#并发数所有都完成或大于50秒就结束  
def callBack(threadName):
    print(threadName+"finish")
    print("total:%d,succ:%d,fail:%d,except:%d\n"%(TOTAL,SUCC,FAIL,EXCEPT))
    print(HOST,URI)
    print('===========task end===========')
    print("total:%d,succ:%d,fail:%d,except:%d"%(TOTAL,SUCC,FAIL,EXCEPT))
    print('response maxtime:',MAXTIME)
    print('response mintime',MINTIME)
# print('great than 3 seconds:%d,percent:%0.2f'%(GT3,float(GT3)/TOTAL))
# print('less than 3 seconds:%d,percent:%0.2f'%(LT3,float(LT3)/TOTAL))