import hashlib
from models.users import User

def hashed(text):
    return hashlib.md5(text.encode()).hexdigest()



def authenticate(username,password):
    """
    校验用户的密码和数据库记录是否匹配

    :return:
    """
    if username and password:
        hash_pass = User.get_pass(username)
        return hash_pass and hash_pass ==hashed(password)
    else:
        return False


def register(username,password):
    if User.is_exists(username):
        return {'msg': 'username is exists'}
    else:
        User.add_user(username,hashed(password))
        return 'ok'