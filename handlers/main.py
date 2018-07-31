import tornado.web
from utils import photo

class IndexHandler(tornado.web.RequestHandler):
    """
    首页，关注用户的的图片流
    """
    def get(self, *args, **kwargs):
        self.render('index.html')


class ExploreHandler(tornado.web.RequestHandler):
    """
    发现页，最新上传的所有图片
    """
    def get(self, *args, **kwargs):
        urls = photo.get_images('uploads/thumbs')
        self.render('explore.html', urls=urls)


class PostHandler(tornado.web.RequestHandler):
    """
    单独图片详情页面
    """
    def get(self, post_id):
        self.render('post.html', post_id=post_id)


class UploadHandler(tornado.web.RequestHandler):
    """
    上传图片的接口
    """
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg',None)
        for img in img_files:
            print("got {}".format(img['filename']))
            save_to = 'static/uploads/{}'.format(img['filename'])
            with open(save_to, 'wb') as f:
                f.write(img['body'])
                print(f)
            photo.make_thumb(save_to)
        self.redirect('/explore')
