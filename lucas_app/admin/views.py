from flask.views import View
from flask import render_template, request, current_app, url_for, redirect
from . import admin
from .forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from .. import db
from sqlalchemy import desc
import requests
from flask_login import current_user
# from ..tickets.models import EventsModel

class RenderTemplateView(View):
	def __init__(self, template_name):
		self.template_name = template_name


	def dispatch_request(self):
		return render_template(self.template_name, data=False)

class RenderHomePage(RenderTemplateView):
	def __init__(self, template_name):
		self.template_name = template_name
		
	def dispatch_request(self):
		try:
			if(current_user.is_admin==False):
				return redirect(url_for('users.login_page'))
		except:
			return redirect(url_for('users.login_page'))
		self.data = {}
		self.users = requests.get('http://127.0.0.1:5000/users')
		# print(self.users.text)
		self.data.update({'users': self.users})
		return render_template(self.template_name, data=self.users)
	



# registering routing rules
admin.add_url_rule('/', view_func=RenderHomePage.as_view(
'admin_index', template_name='admin/index.html'))
