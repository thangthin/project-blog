import webapp2
from handler import Handler
from google.appengine.ext import ndb
from models import User, Post, Comment
from blog_routes import BlogRoutes
from webapp2_extras import json
from blog_decorators import user_logged_in, user_own_comment, comment_exists
blog_uri = BlogRoutes()


class CommentHandler(Handler):
    @comment_exists
    @user_own_comment
    def post(self, comment, **kwargs):
        comment_content = self.request.get("comment-content")
        comment.content = comment_content
        comment.put()
        self.response.content_type = 'application/json'
        print 'comment time', comment.created_date
        obj = {
            'success': 'True',
            'updated_date': comment.created_date.isoformat(),
            'comment_content': comment.content
        }
        self.response.write(json.encode(obj))

    @comment_exists
    @user_own_comment
    def delete(self, comment, comment_key, **kwargs):
        print "delete gets called", comment
        comment_key.delete()
        obj = {
            'success': 'True',
        }
        self.response.write(json.encode(obj))
