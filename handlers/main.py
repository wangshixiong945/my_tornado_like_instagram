import tornado.web
from utils import photo
from utils.account import get_user
from pycket.session import SessionMixin

class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    """
    使用了pycket 来提供 session的 Base

    """
    def get_current_user(self):
        return self.session.get('tudo_user', None)


class IndexHandler(AuthBaseHandler):
    """
    首页，关注用户的的图片流
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = photo.get_posts_for(self.current_user)
        self.render('index.html', posts=posts)


class ExploreHandler(AuthBaseHandler):
    """
    发现页，最新上传的所有图片
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = photo.get_posts()
        self.render('explore.html', posts=posts)


class ProfileHandler(AuthBaseHandler):
    """
    用户信息页面
    """
    @tornado.web.authenticated
    def get(self):
        name = self.get_argument('name', None)
        if not name:
            name = self.current_user
        user = get_user(name)
        if not user:
            self.set_status(404)
            self.write('name 出错')
        else:
            like_posts = photo.get_like_posts(user.id)

            self.render('profile.html', user=user, like_posts=like_posts)


class PostHandler(AuthBaseHandler):
    """
    单独图片详情页面
    """
    @tornado.web.authenticated
    def get(self, post_id):

        post = photo.get_post(post_id)
        users = photo.get_like_users(post.id)
        self.render('post.html', post=post, users=users)


class UploadHandler(AuthBaseHandler):
    """
    上传图片的接口
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg',None)
        for img in img_files:
            # print("got {}".format(img['filename']))
            im = photo.UploadImage(self.settings['static_path'],img['filename'])
            im.save_upload(img['body'])

            #save_to = 'static/uploads/{}'.format(img['filename'])
            # with open(save_to, 'wb') as f:
            #     f.write(img['body'])
            #     print(f)
            im.make_thumb()
            photo.add_post(self.current_user, im.upload_url,im.thumb_url)
            # photo.make_thumb(save_to)
        self.redirect('/explore')
