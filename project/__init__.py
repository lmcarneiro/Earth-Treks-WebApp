# -*- coding: utf-8 -*-
#################
#### imports ####
#################

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_apscheduler import APScheduler
import os

################
#### config ####
################

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(os.environ['APP_SETTINGS'])
#app.run(host='0.0.0.0', port=os.environ.get('PORT'))
db = SQLAlchemy(app)
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()

from project.users.views import users_blueprint
from project.home.views import home_blueprint

# register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)

from project.models import User

login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

if __name__ == 'main':
    app.run()
