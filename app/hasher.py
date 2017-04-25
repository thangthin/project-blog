import hashlib
import hmac


class Hasher():
    """Class to store common hashing method for password"""
    @staticmethod
    def hash_password(password, salt):
        hasher = hmac.new(salt, password, hashlib.sha256)
        hashed_pw = hasher.hexdigest()
        return "%s|%s" % (salt, hashed_pw)

    @staticmethod
    def unhash_password(stored_hashed_pw, password_input):
        salt = stored_hashed_pw.split("|")[0]
        return stored_hashed_pw == Hasher.hash_password(password_input, salt)
