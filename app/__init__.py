from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u1ikgtowhsaic:az69mszhgsr8@bryanmarshall.com/dbuzxie9rljc8i'






db = SQLAlchemy(app)
login = LoginManager(app)

from app import routes, models

if __name__ == '__main__':
    app.run(debug=True)