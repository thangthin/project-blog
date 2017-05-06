from functools import wraps
from google.appengine.ext import ndb
from webapp2_extras import json


def post_exists(function):
    """make sure the post exists before processing handler.
       Redirect to 404 if post doesn't exist
    """
    @wraps(function)
    def wrapper(self, post_id):
        print "checking to see if post exists", post_id
        post = None
        try:
            post_key = ndb.Key(urlsafe=post_id)
            post = post_key.get()
        except Exception:
            # show error
            self.redirect('/blog/error')
            return
        if post:
            return function(self, post_id, post, post_key)
        else:
            self.redirect('/blog/error')
            return
    return wrapper


def user_own_post(function):
    """Make sure user own post, if not, redirect to login"""
    @wraps(function)
    def wrapper(self, post_id, *args, **kwargs):
        print "inside user own post decorator"
        post_urlsafe = None
        if post_id:
            post_urlsafe = post_id
        else:
            post_urlsafe = kwargs.get("post_id")
        post_key = ndb.Key(urlsafe=post_urlsafe)
        post = post_key.get()
        if post.username == self.user.username:
            return function(self, post_id)
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
       Return json object to indicate user comment doesn't exist.
       comment_id can be in request body or request uri depending on method
       used.
    """
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        print "inside comment_exists decorator"
        # see if comment_id is passed by uri
        comment_id = kwargs.get("comment_id")
        print comment_id, "comment id from kwargs"
        comment_urlsafe = None
        if comment_id:
            comment_urlsafe = comment_id
        else:
            comment_urlsafe = self.request.get('comment-id')
        try:
            comment_key = ndb.Key(urlsafe=comment_urlsafe)
            comment = comment_key.get()
            print "comment exist!"
        except:
            obj = {
                    'success': 'False',
                    'updated_date': None,
                    'comment_content': "comment does not exist"
                }
            self.response.write(json.encode(obj))
            return  # prevent execution of regular handler
        function(self, comment, comment_key=comment_key, *args, **kwargs)
    return wrapper


def user_own_comment(function):
    """Check user own comment, if not, return json object to
    indicate user don't have permission"""
    @wraps(function)
    def wrapper(self, comment, *args, **kwargs):
        print "inside user_own_comment wrapper"
        if comment.username == self.user.username:
            function(self, comment, *args, **kwargs)
        else:
            obj = {
                'success': 'False',
                'updated_date': None,
                'comment_content': "not owner"
            }
            self.response.write(json.encode(obj))
    return wrapper
