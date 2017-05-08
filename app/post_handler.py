import webapp2
from handler import Handler
from google.appengine.ext import ndb
from webapp2_extras import json
from models import User, Post, Comment
from blog_routes import BlogRoutes
from blog_decorators import post_exists, user_own_post

blog_uri = BlogRoutes()


class PostHandler(Handler):
    """Handle the viewing of a specific post"""
    def save_comment(self, post_key):
        """save comment only if comment content is not empty"""
        comment_input = self.request.get("comment")
        if not comment_input:
            return None
        comment = Comment(parent=post_key,
                          content=comment_input,
                          post_id=post_key.id(),
                          post_url_string=post_key.urlsafe(),
                          username=self.user.username,
                          user_id=self.user.key.id())
        return comment.put()

    @post_exists
    def get(self, post_id, post, post_key):
        """Viewing Specific Post"""
        comments = Comment.query_post(post_key).fetch()
        self.render('blog/post.html',
                    post=post,
                    user=self.user,
                    comments=comments)

    @post_exists
    def post(self, post_id, post, post_key):
        """Create new comment"""
        success = self.save_comment(post_key)
        comments = Comment.query_post(post_key).fetch()
        if not success:
            self.render('blog/post.html',
                        post=post,
                        user=self.user,
                        comments=comments,
                        error="comment can't be empty")
        else:
            self.redirect("/blog/post/"+post_id)
