import glob, os
import uuid
from PIL import Image
from models.users import Post, session, User


class UploadImage(object):
    """
    辅助保存用户上传的图片，生成缩略图，保存图片相关的URL 用来存到数据库
    保证上传图片保存到一个唯一的文件名
    """
    upload_dir = 'uploads'
    thumb_dir = 'thumbs'
    thumb_size = (200,200)

    def __init__(self, static_path, upload_name):
        """
        记录保存图片的文件路径，把static目录分离出来，保存的路径是相对static的目录，然后展示的时候用static_url去处理
        """
        self.static_path = static_path
        self.upload_name = upload_name
        self.name = self.gen_name()

    def gen_name(self):
        """
        生成一个随意的唯一的字符串，作为图片名字
        """
        _, ext = os.path.splitext(self.upload_name)
        return uuid.uuid4().hex + ext

    @property
    def save_to(self):
        """
        图片文件写入路径
        """
        return os.path.join(self.static_path,self.upload_url)

    def save_upload(self, content):
        with open(self.save_to, 'wb') as f:
            f.write(content)

    @property
    def upload_url(self):
        return os.path.join(self.upload_dir,self.name)

    def make_thumb(self):
        im = Image.open(self.save_to)
        im.thumbnail(self.thumb_size)
        im.save(os.path.join(self.static_path,self.thumb_url),'JPEG')

    @property
    def thumb_url(self):
        filename,ext = os.path.splitext(self.name)
        return os.path.join(
            self.upload_dir,
            self.thumb_dir,
            '{}_{}×{}{}'.format(
                filename,
                self.thumb_size[0],
                self.thumb_size[1],
                ext
            )
        )

def add_post(username,image_url,thumb_url):
    """
    增加一个图片信息到数据库
    :param user_id:
    :param image_url:
    :return:
    """
    user = session.query(User).filter_by(name=username).first()
    post = Post(image_url=image_url, thumb_url=thumb_url, user_id=user.id)
    session.add(post)
    session.commit()

def get_posts():
    posts = session.query(Post).all()
    return posts

def get_posts_for(username):
    user = session.query(User).filter_by(name=username).scalar()
    return user.posts


def get_post(post_id):
    post = session.query(Post).filter_by(id=post_id).scalar()
    return post