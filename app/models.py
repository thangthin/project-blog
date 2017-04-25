from google.appengine.ext import ndb


class User(ndb.Model):
    username = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now=True)
    password = ndb.StringProperty()
    email = ndb.StringProperty()


class Post(ndb.Model):
    username = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now=True)
    subject = ndb.StringProperty()
    content = ndb.TextProperty()
