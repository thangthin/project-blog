from google.appengine.ext import ndb


class User(ndb.Model):
    """Entity to represent user"""
    username = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now=True)
    password = ndb.StringProperty()
    email = ndb.StringProperty()


class Post(ndb.Model):
    """Entity to represent Post"""
    username = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(auto_now=True)
    subject = ndb.StringProperty()
    content = ndb.TextProperty()
    vote = ndb.IntegerProperty()


class Comment(ndb.Model):
    """Models an individual comment entry with content and date."""
    content = ndb.StringProperty()
    username = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    content = ndb.StringProperty()
    post_url_string = ndb.StringProperty()
    post_id = ndb.IntegerProperty()
    created_date = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def query_post(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.created_date)