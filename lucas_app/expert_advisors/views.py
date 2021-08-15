from flask.views import View
from flask import render_template, request, current_app
from . import ea_api, ea
from .ea_resource import EAResource
from .serials_resource import SerialsResource
from .. import db
from sqlalchemy import desc
import uuid


class RenderTemplateView(View):
	def __init__(self, template_name):
		self.template_name = template_name


	def dispatch_request(self):
		return render_template(self.template_name, data=False)


def serial_generator():
	return str(uuid.uuid4())
	

ea.add_url_rule('/serial_gen', 'gen_serial', serial_generator)
ea_api.add_resource(EAResource, '')
ea_api.add_resource(SerialsResource, '/serials')