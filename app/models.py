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

class Asset_Class(db.Model):
    asset_class_id = db.Column(db.Integer, primary_key=True)
    asset_class_name = db.Column(db.String(164), index=True, unique=True)
    allocation_percent = db.Column(db.Float)

class Ticker(db.Model):
    ticker_id = db.Column(db.Integer, primary_key=True)
    ticker_symbol = db.Column(db.String(64), index=True, unique=True)
    company_name = db.Column(db.String(164), index=True)
    current_price = db.Column(db.Float)
    user_id = db.Column(db.Integer)
    asset_class_id = db.Column(db.Integer)
