import webapp2
from handler import Handler
from google.appengine.ext import ndb
from blog_routes import BlogRoutes
from models import User
from blog_decorators import user_own_post, user_logged_in, post_exists
blog_uri = BlogRoutes()


class PostEditHandler(Handler):
    """Handle getting the post edit form and updating specific post"""
    @post_exists
    @user_own_post
    def get(self, post_id):
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        self.render('blog/post_edit.html', post=post, user=self.user)

    @post_exists
    @user_own_post
    def post(self, post_id):
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        post.subject = self.request.get('subject')
        post.content = self.request.get('content')
        post.put()
        uri_post = webapp2.uri_for(blog_uri.post_uri_name, post_id=post_id)
        self.redirect(uri_post)

