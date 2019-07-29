import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate 
from flask_moment import Moment
from bambiv3.config import Config


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
#migrate = Migrate(app, db)
moment = Moment()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'



def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	login_manager.init_app(app)
	bcrypt.init_app(app)
	mail.init_app(app)
	moment.init_app(app)

	from bambiv3.users.routes import users
	from bambiv3.posts.routes import posts
	from bambiv3.main.routes import main
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)

	return app

