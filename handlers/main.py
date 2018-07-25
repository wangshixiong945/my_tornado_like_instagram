import tornado.web

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
        self.render('explore.html')


class PostHandler(tornado.web.RequestHandler):
    """
    单独图片详情页面
    """
    def get(self, post_id):
        self.render('post.html', post_id=post_id)