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
    def post(self, comment_passed):
        # TODO: use passed in comment
        comment_urlsafe = self.request.get('comment-id')
        comment_content = self.request.get("comment-content")
        comment_key = ndb.Key(urlsafe=comment_urlsafe)
        comment = comment_key.get()
        comment.content = comment_content
        comment.put()
        print "comment passed", comment_passed
        self.response.content_type = 'application/json'
        print 'comment time', comment.created_date

        obj = {
            'success': 'True',
            'updated_date': comment.created_date.isoformat(),
            'comment_content': comment.content
        }
        self.response.write(json.encode(obj))

    def delete(self, comment_id):
        print "delete gets called", comment_id
        # get comment
        ndb.Key(urlsafe=comment_id).delete()
        # delete comment
        obj = {
            'success': 'True',
        }
        self.response.write(json.encode(obj))
        # comment_id = self.request.get('comment-id')
        # print "request received to delete comment", comment_id
