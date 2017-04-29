# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import webapp2

from app.blog_routes import BlogRoutes
from app.main_page_handler import MainPage
from app.sign_up_handler import SignupHandler
from app.welcome_handler import WelcomeHandler
from app.login_handler import LoginHandler
from app.logout_handler import LogoutHandler
from app.new_post_handler import NewPostHandler
from app.post_handler import PostHandler
from app.post_edit_handler import PostEditHandler
from app.post_delete_handler import PostDeleteHandler
from app.post_delete_success_handler import PostDeleteSuccessHandler
from app.comment_handler import CommentHandler
from app.vote_handler import VoteHandler
blog_uri = BlogRoutes()

app = webapp2.WSGIApplication([
    ('/', MainPage),
    webapp2.Route(r'/blog/signup',
                  handler=SignupHandler,
                  name=blog_uri.signup_uri_name),
    webapp2.Route(r'/blog/welcome',
                  handler=WelcomeHandler,
                  name=blog_uri.welcome_uri_name),
    webapp2.Route(r'/blog/login',
                  handler=LoginHandler,
                  name=blog_uri.login_uri_name),
    webapp2.Route(r'/blog/logout',
                  handler=LogoutHandler,
                  name=blog_uri.logout_uri_name),
    webapp2.Route(r'/blog/newpost',
                  handler=NewPostHandler,
                  name=blog_uri.new_post_uri_name),
    webapp2.Route(r'/blog/post/<post_id:\S+>',
                  handler=PostHandler,
                  name=blog_uri.post_uri_name),
    webapp2.Route(r'/blog/edit/post/<post_id:\S+>',
                  handler=PostEditHandler,
                  name=blog_uri.post_edit_uri_name),
    webapp2.Route(r'/blog/delete/post/success',
                  handler=PostDeleteSuccessHandler,
                  name=blog_uri.post_delete_success_uri_name),
    webapp2.Route(r'/blog/delete/post/<post_id:\S+>',
                  handler=PostDeleteHandler,
                  name=blog_uri.post_delete_uri_name),
    webapp2.Route(r'/blog/comment/<comment_id:\S+>',
                  handler=CommentHandler,
                  name='comment-delete-api'),
    webapp2.Route(r'/blog/comment/',
                  handler=CommentHandler,
                  name='comment-api'),
    webapp2.Route(r'/blog/postvote/',
                  handler=VoteHandler,
                  name='post-vote-api'),

], debug=True)
