from functools import wraps


def post_exists(function):
    @wraps(function)
    def wrapper(self, post_id):
        print "checking to see if post exists"
        return function(self, post_id)
    return wrapper


def user_logged_in(function):
    @wraps(function)
    def wrapper(self, *args):
        print "checking to see if user is logged in"
        function(self, *args)
        pass
    return wrapper
