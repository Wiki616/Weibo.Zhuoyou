from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    username = db.Column(db.String(128) , primary_key = True)
    nickname = db.Column(db.String(128) , index = True)
    email = db.Column(db.String(128) , index = True)
    password = db.Column(db.String(256) , index = True)
    role = db.Column(db.SmallInteger ,default = ROLE_USER)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


