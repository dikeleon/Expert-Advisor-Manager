from flask.views import View
from flask import render_template, request, current_app
from . import home
from .forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from .. import db
from sqlalchemy import desc
from ..tickets.models import EventsModel

class RenderTemplateView(View):
	def __init__(self, template_name):
		self.template_name = template_name


	def dispatch_request(self):
		return render_template(self.template_name, data=False)

class RenderHomePage(RenderTemplateView):
	def __init__(self, template_name):
		self.template_name = template_name
		
	def dispatch_request(self):
		self.data = {}
		self.events = EventsModel.query.all()
		self.data.update({'events': self.events})
		return render_template(self.template_name, data=self.data)
	



# registering routing rules
home.add_url_rule('/', view_func=RenderHomePage.as_view(
'home_page', template_name='frontend/index.html'))
