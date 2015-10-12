__author__ = 'triThirty'

import os
from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.websocket
import json
import redis

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
if django.VERSION[1] > 5:
    django.setup()

define('port', type=int, default=8080)

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado')

class ChatRoomHandler1(tornado.websocket.WebSocketHandler):
    client=set()
    rds0 = redis.StrictRedis()
    def check_origin(self, origin):
        return True
    def open(self):
        v=self.get_cookie("uid")
        client = ChatRoomHandler1.rds0.hmget(v,("nick_name"))
        if(client[0]):
            dic={}
            info={}
            dic["type"]="sys-online"
            info["nick_name"]=client[0].decode("utf-8")
            dic["info"]=info
            # json_oj = json.dumps(dic)
            self.write_message(dic)
            ChatRoomHandler1.send_to_all(dic)
            ChatRoomHandler1.client.add(self)
        else:
            self.close()
    def on_message(self, message):
        v=self.get_cookie("uid")
        client = ChatRoomHandler1.rds0.hmget(v,("avatar","nick_name"))
        if(client):
            message=message.replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("&","&amp;")
            dic={}
            info={}
            dic["type"]="user"
            info["msg"]=message
            info["avatar"]=client[0].decode("utf-8") #redits缓存
            info["nick_name"]=client[1].decode("utf-8") #redits缓存
            dic["info"]=info
            ChatRoomHandler1.send_to_all(dic)
        else:
            self.close()
    def send_to_all(message):
        for c in ChatRoomHandler1.client:
            c.write_message(message)
    def on_close(self):
        try:
            ChatRoomHandler1.client.remove(self)
            v=self.get_cookie("uid")
            client = ChatRoomHandler1.rds0.hmget(v,("nick_name"))
            dic={}
            info={}
            dic["type"]="sys-offline"
            info["nick_name"]=client[0].decode("utf-8")
            dic["info"]=info
            ChatRoomHandler1.send_to_all(dic)
        except:
            pass


def main():
  parse_command_line()
  wsgi_app = tornado.wsgi.WSGIContainer(
    django.core.handlers.wsgi.WSGIHandler())#TODO 如何找到dollars
  tornado_app = tornado.web.Application(
    [
      ('/testChatroom',ChatRoomHandler1),
      ('/hello-tornado', HelloHandler),
      ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),

      ])
  server = tornado.httpserver.HTTPServer(tornado_app)
  server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
  main()