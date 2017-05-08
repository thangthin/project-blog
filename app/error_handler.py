import webapp2
from handler import Handler
from google.appengine.ext import ndb
from models import User, Post, Comment, Voter
from blog_routes import BlogRoutes
from webapp2_extras import json
blog_uri = BlogRoutes()


class ErrorHandler(Handler):
    """Show user the error encountered"""
    def get(self):
        print "inside error handler", self.request.path
        if self.request.path == '/blog/error/permission':
            self.render('blog/permission_error.html')
        elif self.request.path == '/blog/error/resource':
            self.render('blog/resource_not_found_error.html')

