from handler import Handler
from google.appengine.ext import ndb


class PostHandler(Handler):
    def get(self, post_id):
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        self.render('blog/post.html', post=post)