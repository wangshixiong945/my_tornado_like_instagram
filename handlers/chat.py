import logging
import tornado.escape
# import tornado.ioloop
# import tornado.options
import tornado.web
import tornado.websocket
import uuid

from .main import AuthBaseHandler

class RoomHandler(AuthBaseHandler):
    """
    聊天室页面
    """
    @tornado.web.authenticated
    def get(self):
        self.render("room.html", messages=ChatSocketHandler.msg_list_cache)


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    """
    处理websocket请求和响应，ws客户端连接  /ws 接口
    """
    waiters = set()    # 等待接收信息的用户
    msg_list_cache = []         # 存放消息
    cache_size = 200   # 消息列表的大小

    def get_compression_options(self):
        """ 非 None 的返回值开启压缩 """
        return {}

    def open(self):
        """ 新的WebSocket连接打开，自动调用 """
        logging.info("new connection %s" % self)
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        """ WebSocket连接断开，自动调用 """
        ChatSocketHandler.waiters.remove(self)
        logging.info("connection close %s" % self)

    @classmethod
    def update_cache(cls, chat):
        """更新消息列表，加入新的消息"""
        cls.msg_list_cache.append(chat)
        if len(cls.msg_list_cache) > cls.cache_size:
            cls.msg_list_cache = cls.msg_list_cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        """给每个等待接收的用户发新的消息"""
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        """ WebSocket 服务端接收到消息，自动调用 """
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
        }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)