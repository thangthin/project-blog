import webapp2
from handler import Handler
from google.appengine.ext import ndb
from blog_routes import BlogRoutes
from models import User
from blog_decorators import user_own_post, user_logged_in
blog_uri = BlogRoutes()


class PostEditHandler(Handler):
    @user_logged_in
    @user_own_post
    def get(self, post_id):
        authenticated = self.authenticate()
        authorized = self.is_authorize(post_id)
        if authenticated and authorized:
            post_key = ndb.Key(urlsafe=post_id)
            post = post_key.get()
            self.render('blog/post_edit.html', post=post, user=self.user)
        else:
            uri_welcome = webapp2.uri_for(blog_uri.welcome_uri_name)
            self.redirect(uri_welcome)

    def post(self, post_id):
        authenticated = self.authenticate()
        authorized = self.is_authorize(post_id)
        if authenticated and authorized:
            post_key = ndb.Key(urlsafe=post_id)
            post = post_key.get()
            post.subject = self.request.get('subject')
            post.content = self.request.get('content')
            post.put()
            uri_post = webapp2.uri_for(blog_uri.post_uri_name, post_id=post_id)
            self.redirect(uri_post)
        else:
            uri_welcome = webapp2.uri_for(blog_uri.welcome_uri_name)
            self.redirect(uri_welcome)
