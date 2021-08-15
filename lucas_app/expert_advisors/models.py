from lucas_app import db
import datetime


class EAModel(db.Model):
	"""EA Model"""
	__tablename__ = 'expert_advisors'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(90))
	description = db.Column(db.Text)
	photo = db.Column(db.Text)
	added_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class SerialsModel(db.Model):
        
	""""Serial Keys Model"""
	__tablename__ = "serial_keys"
	id = db.Column(db.Integer, primary_key=True)
	ea_id = db.Column(db.Integer, db.ForeignKey(
	    "expert_advisors.id"), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey(
	    "users.id"), nullable=False)
	broker_login = db.Column(db.Integer, unique=True)
	s_key = db.Column(db.String(90), unique=True)
	is_active = db.Column(db.Boolean)
	added_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	due_date = db.Column(db.DateTime)


