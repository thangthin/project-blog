import webapp2
import jinja2
import os
from models import User, Post
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    def authenticate(self):
        try:
            cookie = self.request.cookies["user_auth"]
            cookie_list = cookie.split("|")
            user_id = int(cookie_list[0])
            salt = cookie_list[1]
            hashed_pw = cookie_list[2]
            user_cred = User.get_by_id(user_id).password
            print user_cred, "###<----------"
            return user_cred == "|".join(cookie_list[1:])
        except Exception:
            print "exception thrown"
            return False

    def get_username(self):
        try:
            cookie = self.request.cookies["user_auth"]
            cookie_list = cookie.split("|")
            user_id = int(cookie_list[0])
            user = User.get_by_id(user_id)
            return user.username
        except Exception:
            return None

    def get_userid(self):
        return self.get_user().key.id()

    def get_user(self):
        try:
            cookie = self.request.cookies["user_auth"]
            cookie_list = cookie.split("|")
            user_id = int(cookie_list[0])
            user = User.get_by_id(user_id)
            return user
        except Exception:
            return None

    def is_authorize(self, post_id):
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        return self.get_username() == post.username

    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))
