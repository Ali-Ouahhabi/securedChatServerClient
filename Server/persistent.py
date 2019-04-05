from tinydb import TinyDB, Query


class transaction:
    def __init__(self, Path):
        self.db = TinyDB(Path)
        self.Q = Query()

    def insert(self, usn, pswd):
        res = self.db.search(self.Q.user == usn)
        if self.is_in(usn, pswd):
            return False
        else:
            self.db.insert({'user': usn, 'password': pswd})
            return True

    def is_in(self, usn, pswd):
        res = self.db.search((self.Q.user == usn) & (self.Q.password == pswd))
        if len(res) != 0:
            return True
        else:
            return False
