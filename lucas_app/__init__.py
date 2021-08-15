from lucas_app.config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_principal import Principal, Permission, RoleNeed
from flask_images import Images
from flask_jwt_extended import JWTManager

login_manager = LoginManager()
db = SQLAlchemy()
api = Api()
ma = Marshmallow()
migrate = Migrate()
mail = Mail()


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	api.init_app(app)
	db.init_app(app)
	ma.init_app(app)
	mail.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)
	from .users import users as users_blueprint
	from .expert_advisors import ea as ea_blueprint
	from .auth import auth as auth_blueprint
	from .admin import admin as admin_blueprint
	

	app.register_blueprint(ea_blueprint, url_prefix='/ea')
	app.register_blueprint(users_blueprint, url_prefix='/users')
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	app.register_blueprint(admin_blueprint, url_prefix='/admin')
	return app
