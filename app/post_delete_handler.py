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
        authenticated = self.authenticate()
        authorized = self.is_authorize(post_id)
        if authenticated and authorized:
            post_key = ndb.Key(urlsafe=post_id)
            post = post_key.get()
            self.render('blog/post_delete.html', post=post)
        else:
            uri_welcome = webapp2.uri_for(blog_uri.welcome_uri_name)
            self.redirect(uri_welcome)

    @post_exists
    @user_own_post
    def post(self, post_id):
        authenticated = self.authenticate()
        authorized = self.is_authorize(post_id)
        if authenticated and authorized:
            post_key = ndb.Key(urlsafe=post_id)
            post = post_key.get()
            post.key.delete()
            print "about to delete post:", post_id
            self.redirect('/blog/delete/post/success')
        else:
            uri_welcome = webapp2.uri_for(blog_uri.welcome_uri_name)
            self.redirect(uri_welcome)
