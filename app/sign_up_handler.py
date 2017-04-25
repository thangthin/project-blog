import re
import webapp2
from handler import Handler
from models import User, Post
from blog_routes import BlogRoutes
from hasher import Hasher

blog_uri = BlogRoutes()


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
            uri_welcome = webapp2.uri_for(blog_uri.welcome_uri_name)
            self.set_cookie("user_auth", str(user_id) + "|" + hashed_value)
            self.redirect(uri_welcome)
        else:
            self.render("blog/signup.html", errors=errors)