import webapp2
from handler import Handler
from google.appengine.ext import ndb
from webapp2_extras import json
from models import User, Post, Comment
from blog_routes import BlogRoutes
from blog_decorators import post_exists, user_own_post

blog_uri = BlogRoutes()


class PostHandler(Handler):
    @post_exists
    def get(self, post_id, post, post_key):
        """Viewing Specific Post"""
        comments = Comment.query_post(post_key).fetch()
        self.render('blog/post.html',
                    post=post,
                    user=self.user,
                    comments=comments)

    def post(self, post_id):
        """TODO: FIX This to creat new post instead of Creating comment!!!!!"""
        print "inside creating a post of post handler"
        user = self.get_user()
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        post_id_num = post.key.id()
        ancestor_key = ndb.Key('Post', post_id_num or '*notitle*')

        parent_key = ndb.Key("Post", post_id_num)
        comment = Comment(parent=parent_key)
        comment_input = self.request.get("comment")
        comment.content = comment_input
        comment.post_id = post_id_num
        comment.post_url_string = post_id
        comment.username = user.username
        comment.user_id = user.key.id()
        comment.put()
        self.redirect("/blog/post/"+post_id)

    @post_exists
    def put(self, post_id, post, *args):
        """Update post with post_id"""
        print "inside post handler put method"
        post_key = ndb.Key(urlsafe=post_id)
        post = post_key.get()
        post.subject = self.request.get('subject')
        post.content = self.request.get('content')
        post.put()
        obj = {
            'success': 'True',
            'action': 'redirect',
            'redirect_path': '/blog/post/{0}'.format(post_id)
        }
        self.response.write(json.encode(obj))

