from functools import wraps
from google.appengine.ext import ndb
from webapp2_extras import json

def post_exists(function):
    """make sure the post exists before processing handler.
       Redirect to 404 if post doesn't exist
    """
    @wraps(function)
    def wrapper(self, post_id):
        print "checking to see if post exists"
        try:
            post_key = ndb.Key(urlsafe=post_id)
            post = post_key.get()
            if post:
                return function(self, post_id, post, post_key)
        except Exception:
            # show error
            self.redirect('/blog/error')
            return
    return wrapper


def user_own_post(function):
    """Make sure user own post, if not, redirect to login"""
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        post_id = kwargs.get("post_id")
        print "inside user_own_post", post_id
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        if post.username == self.user.username:
            return function(self, *args, **kwargs)
        else:
            self.redirect('/blog/error')
            return
    return wrapper


def user_logged_in(function):
    """Check to see if user is logged in"""
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        print "checking to see if user is logged in"
        if self.authenticate():
            return function(self, *args, **kwargs)
        else:
            self.redirect('/blog/logout')
            return
    return wrapper


def comment_exists(function):
    """Make sure requested comment exist before processing handler,
       Return json object to indicate user comment doesn't exist
    """
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        print "inside comment_exists decorator"
        try:
            comment_urlsafe = self.request.get('comment-id')
            comment_key = ndb.Key(urlsafe=comment_urlsafe)
            comment = comment_key.get()
        except Exception:
            obj = {
                'success': 'False',
                'updated_date': None,
                'comment_content': "comment does not exist"
            }
            self.response.write(json.encode(obj))
            return  # prevent execution of regular handler
        function(self, comment_passed=comment, *args, **kwargs)
    return wrapper


def user_own_comment(function):
    """Check user own comment, if not, return json object to
    indicate user don't have permission"""
    @wraps(function)
    def wrapper(self, comment_passed, *args, **kwargs):
        print "inside user_own_comment wrapper"
        print "wonder if comment_passed gets to second decorator:", comment_passed
        comment_urlsafe = self.request.get('comment-id')
        comment_key = ndb.Key(urlsafe=comment_urlsafe)
        comment = comment_key.get()
        if comment.username == self.user.username:
            function(self, comment_passed, *args, **kwargs)
        else:
            obj = {
                'success': 'False',
                'updated_date': comment.created_date.isoformat(),
                'comment_content': "not owner"
            }
            self.response.write(json.encode(obj))
    return wrapper
