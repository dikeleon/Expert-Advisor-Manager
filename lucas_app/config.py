# class Config:
# 	ENV = 'development'
# 	SECRET_KEY = '123456789'
# 	SQLALCHEMY_DATABASE_URI = 'mysql://root:""@localhost/intelliCommerce'
# 	SQLALCHEMY_ECHO = 'True'
# 	SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	# FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	# FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
	# FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'dikeleon@gmail.com'
	MAIL_PASSWORD = ''
	ENV = 'development'
	SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/lucas_app'
	SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
	IMAGE_UPLOADS = os.path.join(basedir, 'static/image_uploads')
	# JWT CONFIGURATIONS
	JWT_SECRET_KEY = 'supersecretkeywhateverwhatever'
	SECRET_KEY = 'thisisasecretkeyguyshackitifyouwantto'
	JWT_CSRF_IN_COOKIES = True
	JWT_TOKEN_LOCATION = ['cookies']
	JWT_COOKIE_SECURE = False
	JWT_ACCESS_COOKIE_PATH = '/auth/token_api/'
	JWT_REFRESH_COOKIE_PATH = 'auth/token/refresh'
	JWT_COOKIE_CSRF_PROTECT = True


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
