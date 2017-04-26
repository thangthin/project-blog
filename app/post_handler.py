from handler import Handler
from google.appengine.ext import ndb
from models import User


class PostHandler(Handler):
    def get(self, post_id):
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        user = self.get_user()
        self.render('blog/post.html', post=post, user=user)