import datetime


class User:
    def __init__(self,
                 username,
                 salt,
                 password_hash,
                 email_id=None,
                 is_admin=0,
                 currently_loggedin = 0):
        self._username = username
        self._salt = salt
        self._password_hash = password_hash
        self._created_time = str(datetime.datetime.utcnow())
        self._email_id = email_id
        #is_admin is 0, then it is false
        self._is_admin = is_admin
        # currently_loggedin is 0, then it is false
        self._currently_loggedin = 0

    def get_salt(self):
        return self._salt

    def get_hash(self):
        return self._password_hash

    def get_username(self):
        return self._username

    def get_email_id(self):
        return self._email_id

    def is_admin(self):
        return self._is_admin

    def get_currently_loggedin(self):
        return self._currently_loggedin

    def get_created_time(self):
        return self._created_time
