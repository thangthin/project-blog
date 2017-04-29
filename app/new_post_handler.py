import webapp2
from models import User, Post, Voter
from handler import Handler
from blog_routes import BlogRoutes
blog_uri = BlogRoutes()


class NewPostHandler(Handler):
    def get_user_name(self):
        cookie = self.request.cookies["user_auth"]
        user_id = cookie.split("|")[0]
        username = User.get_by_id(int(user_id)).username
        return username

    def save_post(self, username, subject, content):
        post = Post(voters=[Voter(username=username)])
        post.username = username
        post.subject = subject
        post.content = content
        post.vote = 0
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
        uri_post = webapp2.uri_for(blog_uri.post_uri_name,
                                   post_id=url_safe_post)
        self.redirect(uri_post)