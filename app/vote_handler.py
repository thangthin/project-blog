import webapp2
from handler import Handler
from google.appengine.ext import ndb
from models import User, Post, Comment
from blog_routes import BlogRoutes
from webapp2_extras import json
blog_uri = BlogRoutes()


class VoteHandler(Handler):
    """Use to update vote count in a post"""
    def put(self):
        post_id = self.request.get('post-id')
        post = ndb.Key(urlsafe=post_id).get()
        # allow previous posts in production to have vote
        if not post.vote:
            post.vote = 0
        post.vote = post.vote + 1
        post.put()
        obj = {
            'success': 'True',
            'updated_vote': post.vote
        }
        self.response.write(json.encode(obj))

