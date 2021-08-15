from lucas_app import db, ma
from flask_restful import Resource
from .models import UsersModel
from werkzeug.utils import secure_filename
from flask import redirect, request, current_app as app, flash, url_for, jsonify
import os, uuid
from ..expert_advisors.models import EAModel, SerialsModel


class userSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsersModel
        fields = ['id', 'full_name', 'email', 'phone', 'expert_advisor', 'bound_acc', 's_key', 'is_active']

class UserMiscResource(Resource):

    def get(self):
        try:
            id = request.args['id']
            # get_user = UsersModel.query.filter_by(id = id).all()
            get_user = db.session.query(UsersModel.full_name, UsersModel.id, UsersModel.email, UsersModel.phone, EAModel.name.label('expert_advisor'), SerialsModel.broker_login.label('bound_acc'), SerialsModel.s_key, SerialsModel.is_active).filter_by(id = id).outerjoin(SerialsModel, UsersModel.id==SerialsModel.user_id).outerjoin(EAModel, SerialsModel.ea_id==EAModel.id).all()
        except:
            get_user = db.session.query(UsersModel.full_name, UsersModel.id, UsersModel.email, UsersModel.phone, EAModel.name.label('expert_advisor'), SerialsModel.broker_login.label('bound_acc'), SerialsModel.s_key, SerialsModel.is_active).outerjoin(SerialsModel, UsersModel.id==SerialsModel.user_id).outerjoin(EAModel, SerialsModel.ea_id==EAModel.id).all() 
        user_schema = userSchema(many=True)
        output = user_schema.dump(get_user)
        return output
        
