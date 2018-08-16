import tornado.web
import tornado.gen
from tornado.httpclient import HTTPClient, AsyncHTTPClient
from .main import AuthBaseHandler
from utils import photo
from datetime import datetime



class AsyncSaveURLHandler(AuthBaseHandler):
    """
    保存指定的图片URL(异步版本)
    """
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        url = self.get_argument('url', '')
        async_client = AsyncHTTPClient()
        resp = yield async_client.fetch(url)
        im = photo.UploadImage(self.settings['static_path'], 'x.jpg')
        print(resp.body)
        if not resp.body:
            self.write('empty response')
            return
        im.save_upload(resp.body)
        im.make_thumb()
        post = photo.add_post(self.current_user, im.upload_url, im.thumb_url)
        print("--{}--end fetch:#{}".format(datetime.now(),post.id))
        self.redirect('/post/{}'.format(post.id))


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
