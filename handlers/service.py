import tornado.web
import tornado.gen
from tornado.httpclient import HTTPClient, AsyncHTTPClient
from .main import AuthBaseHandler
from utils import photo
import uuid
import tornado.escape
from .chat import WSocketHandler
from datetime import datetime



class AsyncSaveURLHandler(AuthBaseHandler):
    """
    保存指定的图片URL(异步版本)
    """
    # @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        url = self.get_argument('url', '')
        post_user = self.get_argument('user',None)
        is_room = self.get_argument('from', None) == 'room'

        if not (is_room and post_user):
            print("no user no room--{}{}:{}".format(datetime.now(), post_user, url))
            return

        async_client = AsyncHTTPClient()
        print("--{}-start fetch:{}".format(datetime.now(), url))
        resp = yield async_client.fetch(url,request_timeout=60)

        if not resp.body:
            self.write('empty response')
            return

        im = photo.UploadImage(self.settings['static_path'], 'x.jpg')
        im.save_upload(resp.body)
        im.make_thumb()
        post = photo.add_post(post_user, im.upload_url, im.thumb_url)
        print("--{}--end fetch:#{}".format(datetime.now(),post.id))

        body = '{}post: http://127.0.0.1:8000/post/{}'.format(post_user,post.id)
        chat_msg = WSocketHandler.make_html(body, img=post.thumb_url)
        chat_msg["html"] = tornado.escape.to_basestring(
            self.render_string("include/message.html", message=chat_msg))

        WSocketHandler.update_cache(chat_msg)
        WSocketHandler.send_updates(chat_msg)
        print("message sent!")


class SaveURLHandler(AuthBaseHandler):
    """
    保存指定的图片URL（同步版本）
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        url = self.get_argument('url', '')
        client = HTTPClient()
        print("---going to fetch:{}".format(url))
        resp = client.fetch(url)
        im = photo.UploadImage(self.settings['static_path'], 'x.jpg')
        im.save_upload(resp.body)
        im.make_thumb()
        post = photo.add_post(self.current_user,im.upload_url,im.thumb_url)
        self.redirect('/post/{}'.format(post.id))
