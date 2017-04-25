import re
import webapp2
from handler import Handler
from models import User, Post
from blog_routes import BlogRoutes
blog_uri = BlogRoutes()


class WelcomeHandler(Handler):
    def get_user(self):
        try:
            cookie = self.request.cookies["user_auth"]
            cookie_list = cookie.split("|")
            user_id = int(cookie_list[0])
            user = User.get_by_id(user_id)
            return user
        except Exception:
            return None

    def get(self):
        authorized = self.authenticate()
        if authorized:
            posts = Post.query().order(-Post.created_date).fetch(10)
            user = self.get_user()
            self.render('blog/welcome.html', posts=posts, user=user)
        else:
            uri_signup = webapp2.uri_for(blog_uri.signup_uri_name)
            self.redirect(uri_signup)