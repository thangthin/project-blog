import re
import webapp2
from handler import Handler
from models import User, Post
from blog_routes import BlogRoutes
blog_uri = BlogRoutes()


class WelcomeHandler(Handler):
    """Render welcome page with last 10 posts if user is authenticated
       Redirect user to signup page if not
    """
    def get(self):
        authenticated = self.authenticate()
        if authenticated:
            posts = Post.query().order(-Post.created_date).fetch(10)
            user = self.user
            self.render('blog/welcome.html', posts=posts, user=user)
        else:
            uri_signup = webapp2.uri_for(blog_uri.signup_uri_name)
            self.redirect(uri_signup)
