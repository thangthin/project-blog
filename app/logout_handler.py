import webapp2
from handler import Handler
from blog_routes import BlogRoutes
blog_uri = BlogRoutes()


class LogoutHandler(Handler):
    def get(self):
        self.response.set_cookie('user_auth', '')
        uri_login = webapp2.uri_for(blog_uri.login_uri_name)
        self.redirect(uri_login)