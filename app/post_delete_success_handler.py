import webapp2
from handler import Handler
from google.appengine.ext import ndb
from blog_routes import BlogRoutes
from models import User
blog_uri = BlogRoutes()


class PostDeleteSuccessHandler(Handler):
    def get(self):
        self.render('blog/post_delete_success.html')

