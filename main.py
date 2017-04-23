# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import webapp2
import jinja2
import string
import re
import hashlib
import hmac

from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Hasher():
    # class method
    @staticmethod
    def hash_password(password, salt):
        hasher = hmac.new(salt, password, hashlib.sha256)
        hashed_pw = hasher.hexdigest()
        return "%s|%s" % (salt, hashed_pw)

    @staticmethod
    def unhash_password(stored_hashed_pw, password_input):
        salt = stored_hashed_pw.split("|")[0]
        return stored_hashed_pw == Hasher.hash_password(password_input, salt)


# Model
class User(ndb.Model):
    username = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now=True)
    password = ndb.StringProperty()
    email = ndb.StringProperty()


class Post(ndb.Model):
    username = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now=True)
    subject = ndb.StringProperty()
    content = ndb.TextProperty()


# URL Handler
class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))


class MainPage(Handler):
    def get(self):
        self.render('blog/home.html')

    def post(self):
        pass


class SignupHandler(Handler):
    def is_valid_username(self, username):
        USER_NAME = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_NAME.match(username)

    def is_valid_password(self, password):
        PASSWORD = re.compile(r"^.{3,20}$")
        return PASSWORD.match(password)

    def is_valid_email(self, email):
        EMAIL = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        return EMAIL.match(email)

    def get(self):
        self.render('blog/signup.html')

    def verify_signup_inputs(self, username, password, verify, email):
        errors = []
        # append username error if there
        if not self.is_valid_username(username):
            errors.append("username is not valid")
        # if username is taken
        if User.query(User.username == username).count():
            errors.append("username is already taken")
        # append password is not empty and not valid
        if not self.is_valid_password(password):
            errors.append("password is not valid")
        # append password match error
        if password != verify:
            errors.append("verification did not match password")
        # append email error
        if (len(email) != 0) and (not self.is_valid_email(email)):
            errors.append("email is not valid")
        return errors

    def register_user(self, username, password, email):
        # TODO: reimplement using google datastore urlsafe api
        new_user = User()
        new_user.username = username
        new_user.password = Hasher.hash_password(password, "salt")
        new_user.email = email
        user_key = new_user.put()
        return user_key.id()

    def set_cookie(self, name, value):
        self.response.set_cookie(name, value, max_age=360, path='/')

    def post(self):
        username_input = self.request.get("username")
        password_input = self.request.get("password")
        verify_input = self.request.get("verify")
        email_input = self.request.get("email")
        print username_input, password_input, verify_input, email_input
        errors = self.verify_signup_inputs(username_input,
                                           password_input,
                                           verify_input,
                                           email_input)
        if not errors:
            user_id = self.register_user(username_input,
                                         password_input,
                                         email_input)
            hashed_value = User.get_by_id(user_id).password
            self.set_cookie("user_auth", str(user_id) + "|" + hashed_value)
            self.redirect("/blog/welcome")
        else:
            self.render("blog/signup.html", errors=errors)


class WelcomeHandler(Handler):
    def check_authorization(self):
        try:
            cookie = self.request.cookies["user_auth"]
            cookie_list = cookie.split("|")
            user_id = int(cookie_list[0])
            salt = cookie_list[1]
            hashed_pw = cookie_list[2]
            user_cred = User.get_by_id(user_id).password
            return user_cred == "|".join(cookie_list[1:])
        except Exception:
            return False

    def get(self):
        authorized = self.check_authorization()
        if authorized:
            posts = Post.query().order(-Post.created_date).fetch(10)
            self.render('blog/welcome.html', posts=posts)
        else:
            self.redirect("/blog/signup")


class LoginHandler(Handler):
    def authenticate_user(self, user_account, password_input):
        return Hasher.unhash_password(str(user_account.password),
                                      str(password_input))

    def get(self):
        self.render('blog/login.html')

    def post(self):
        username_input = self.request.get('username')
        password_input = self.request.get('password')
        user_accounts = User.query(User.username == username_input).fetch(1)
        if len(user_accounts) > 0:
            user_account = user_accounts[0]
            authenticated = self.authenticate_user(user_account,
                                                   password_input)
            if authenticated:
                self.response.set_cookie('user_auth',
                                         str(user_account.key.id()) + "|" + user_account.password)  # noqa
                self.redirect('/blog/welcome')
            else:
                self.redirect('/blog/login')
        else:
            self.redirect('/blog/login')


class LogoutHandler(Handler):
    def get(self):
        self.response.set_cookie('user_auth', '')
        self.redirect('/blog/login')


class NewPostHandler(Handler):
    def get_user_name(self):
        cookie = self.request.cookies["user_auth"]
        user_id = cookie.split("|")[0]
        username = User.get_by_id(int(user_id)).username
        return username

    def save_post(self, username, subject, content):
        post = Post()
        post.username = username
        post.subject = subject
        post.content = content
        post_key = post.put()
        url_string = post_key.urlsafe()
        return url_string

    def get(self):
        self.render('blog/newpost.html')

    def post(self):
        username = self.get_user_name()
        subject = self.request.get('subject')
        content = self.request.get('content')
        url_safe_post = self.save_post(username, subject, content)
        uri = webapp2.uri_for('post-page', post_id=url_safe_post)
        self.redirect(uri)


class PostHandler(Handler):
    def get(self, post_id):
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        self.render('blog/post.html', post=post)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog/signup', SignupHandler),
    ('/blog/welcome', WelcomeHandler),
    ('/blog/login', LoginHandler),
    ('/blog/logout', LogoutHandler),
    ('/blog/newpost', NewPostHandler),
    webapp2.Route(r'/blog/post/<post_id:\S+>', handler=PostHandler, name='post-page'),  # noqa
], debug=True)
