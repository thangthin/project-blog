import webapp2
from handler import Handler
from google.appengine.ext import ndb
from blog_routes import BlogRoutes
from models import User
from blog_decorators import user_own_post, post_exists
blog_uri = BlogRoutes()


class PostDeleteHandler(Handler):
    @post_exists
    def get(self, post_id, *args, **kwargs):
        """Show user confirmation on post to delete"""
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        self.render('blog/post_delete.html', post=post)

    @post_exists
    @user_own_post
    def post(self, post_id):
        """Delete post if post exist and user own post"""
        # TODO: implement delete associated comments
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        post.key.delete()
        self.redirect('/blog/delete/post/success')
