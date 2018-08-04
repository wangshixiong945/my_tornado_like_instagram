import tornado.web
from .main import AuthBaseHandler
from utils.account import authenticate, register


class LoginHandler(AuthBaseHandler):
    """
    登录页面
    """
    def get(self, *args, **kwargs):
        next_url = self.get_argument('next', '')
        self.render('login.html', next_url=next_url)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        next_url = self.get_argument('next', '')

        passed = authenticate(username, password)
        if passed:
            self.session.set('tudo_user', username)
            if next_url:
                self.redirect(next_url)
            else:
                self.redirect('/')
        else:
            self.write({'msg':'login fail'})


class LogoutHandler(AuthBaseHandler):
    """
    实现登出，清除 session 信息
    """
    def get(self, *args, **kwargs):
        self.session.delete('tudo_user')
        self.redirect('/login')


class SignupHandler(AuthBaseHandler):
    """
    注册
    """
    def get(self, *args, **kwargs):
        self.render('signup.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password1 = self.get_argument('password1', None)
        password2 = self.get_argument('password2', None)

        if username and password1 and(password1 == password2):

            # save to db
            ret =register(username, password1)
            if ret['msg'] == 'ok':
                self.session.set('tudo_user', username)
                self.redirect('/')
            else:
                self.write(ret)
        else:
            self.write({'msg': 'signup fail'})