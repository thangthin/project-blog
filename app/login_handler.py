import webapp2
from handler import Handler
from models import User
from blog_routes import BlogRoutes
from hasher import Hasher

blog_uri = BlogRoutes()


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
        uri_login = webapp2.uri_for(blog_uri.login_uri_name)
        uri_welcome = webapp2.uri_for(blog_uri.welcome_uri_name)

        if len(user_accounts) > 0:
            user_account = user_accounts[0]
            authenticated = self.authenticate_user(user_account,
                                                   password_input)
            if authenticated:
                self.response.set_cookie('user_auth',
                                         str(user_account.key.id()) + "|" + user_account.password)  # noqa
                self.redirect(uri_welcome)
            else:
                self.redirect(uri_login)
        else:
            self.redirect(uri_login)