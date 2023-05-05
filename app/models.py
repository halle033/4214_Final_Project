from app import db
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

##### USER MODEL #####
# The user_id needs to be named id for the UserMixin to work correctly
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    def get_id(self):
        return (self.id)

class Crypto_Class(db.Model):
    crypto_class_id = db.Column(db.Integer, primary_key=True)
    crypto_class_name = db.Column(db.String(164), index=True, unique=True)
    crypto_percent = db.Column(db.Float)

class Crypto(db.Model):
    crypto_class_id = db.Column(db.Integer, primary_key=True)
    crypto_symbol = db.Column(db.String(64), index=True, unique=True)
    comp_name = db.Column(db.String(164), index=True)
    crypto_price = db.Column(db.Float)
    user_id_ = db.Column(db.Integer)
    crypto_id_ = db.Column(db.Integer)