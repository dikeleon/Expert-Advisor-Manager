from lucas_app import db, login_manager
import datetime
from flask_login import UserMixin
# from flask_security import RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref

class UsersModel(UserMixin, db.Model):
	"""Users Model"""
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(90))
	is_admin = db.Column(db.Boolean)
	is_active = db.Column(db.Boolean)
	email = db.Column(db.String(90))
	phone = db.Column(db.String(30))
	password = db.Column(db.Text)
	confirm_code = db.Column(db.Text)
	photo = db.Column(db.Text)
	dob = db.Column(db.DateTime)
	added_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	def set_password(self, password):
		"""Create hashed password."""
		self.password = generate_password_hash(password, method='sha256')

	def check_password(self, password):
		"""Check hashed password."""
		return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
	return UsersModel.query.get(int(user_id))