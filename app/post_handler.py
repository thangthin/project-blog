import webapp2
from handler import Handler
from google.appengine.ext import ndb
from models import User, Post, Comment
from blog_routes import BlogRoutes
blog_uri = BlogRoutes()


class PostHandler(Handler):
    def get(self, post_id):
        comments_qry = Comment.query(Comment.post_url_string == post_id)
        comments = comments_qry.order(-Comment.created_date).fetch()
        print comments
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        user = self.get_user()
        self.render('blog/post.html', post=post, user=user, comments=comments)

    def post(self, post_id):
        comments_qry = Comment.query(Comment.post_url_string == post_id)
        comments = comments_qry.order(-Comment.created_date).fetch()
        print type(comments)

        comment_input = self.request.get("comment")
        comment = Comment()
        comment.post_url_string = post_id
        comment.username = self.get_username()
        comment.user_id = self.get_userid()
        comment.content = comment_input
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()

        comment.post_id = post.key.id()
        user = self.get_user()
        comment_key = comment.put()
        # manually append to comments list
        # uri_post = webapp2.uri_for(blog_uri.post_uri_name, post_id=post_id)
        # self.redirect(uri_post)
        # list to store all the comments for particular post TODO: implement
        # print comments
        # TODO: Need better implementation as post request is made again when page is refreshed
        comments.insert(0, comment)
        self.render('blog/post.html', post=post, user=user, comments=comments)
        # uri_post = webapp2.uri_for(blog_uri.post_uri_name, post_id=post_id)
        # self.redirect(uri_post)