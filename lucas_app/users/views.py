from flask.views import View
from flask import render_template, request, current_app, redirect, url_for
from . import users_api, users
from .users_resource import UserResource
from ..expert_advisors.models import SerialsModel, EAModel
from .users_resource_misc import UserMiscResource
from .. import db
from sqlalchemy import desc
from flask_login import current_user


class RenderTemplateView(View):
	def __init__(self, template_name):
		self.template_name = template_name


	def dispatch_request(self):
		return render_template(self.template_name, data=False)

class RenderUserPage(RenderTemplateView):
	def __init__(self, template_name):
		self.template_name = template_name
		
	def dispatch_request(self):
		try:
			if(current_user.is_authenticated==False):
				return redirect(url_for('users.login_page'))
		except:
			return redirect(url_for('users.login_page'))

		# ea_data = SerialsModel.query.filter_by(user_id = current_user.id).one()
		ea_data = db.session.query(SerialsModel.broker_login, SerialsModel.s_key, EAModel.name).join(EAModel).filter(SerialsModel.user_id == current_user.id).one()
		return render_template(self.template_name, data=ea_data)

users_api.add_resource(UserResource, '')
users_api.add_resource(UserMiscResource, '/misc')

# routing for contol panel
users.add_url_rule('/cp', view_func=RenderUserPage.as_view(
'user_cp_index', template_name='users/index.html'))

users.add_url_rule('/login', view_func=RenderTemplateView.as_view(
'login_page', template_name='auth/login.html'))

users.add_url_rule('/register', view_func=RenderTemplateView.as_view(
'registration_page', template_name='auth/register.html'))
