from flask import Blueprint
from flask_restful import Api


ea = Blueprint('ea', __name__)
ea_api = Api(ea)

from . import views

