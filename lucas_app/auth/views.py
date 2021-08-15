from flask.views import View
from flask import render_template, request, current_app
from . import auth_api, auth
from .auth_resource import AuthResource, confirm_account, login_account, logout_account
from .. import db
from sqlalchemy import desc


class RenderTemplateView(View):
	def __init__(self, template_name):
		self.template_name = template_name


	def dispatch_request(self):
		return render_template(self.template_name, data=False)




auth_api.add_resource(AuthResource, '')
auth.add_url_rule('/confirm_acc', 'confirm_acc', confirm_account)
auth.add_url_rule('/login', 'login_acc', login_account, methods=['POST'])
auth.add_url_rule('/logout', 'logout_acc', logout_account)

# auth.add_url_rule('/check_serial', 'check_serial', check_serial)