from lucas_app import db, ma
from flask_restful import Resource
from .models import SerialsModel
from werkzeug.utils import secure_filename
from flask import redirect, request, current_app as app, flash, url_for, jsonify
import os, uuid
from flask_sqlalchemy import sqlalchemy
from flask_login import login_required


class serialsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SerialsModel
        fields = ['id', 'ea_id', 'user_id', 'broker_login', 's_key', 'is_active', 'added_on', 'due_date']

class SerialsResource(Resource):

    @login_required
    def get(self):
        try:
            id = request.args['id']
            get_ticket = SerialsModel.query.filter_by(id = id).all()
        except:
            get_ticket = SerialsModel.query.all()
        chapter_schema = serialsSchema(many=True)
        output = chapter_schema.dump(get_ticket)
        return {'serial_keys': output}

    @login_required
    def post(self):
        ea_id = request.form['ea_id']
        user_id = request.form['user_id']
        broker_login = request.form['broker_login']
        s_key = uuid.uuid4()
        due_date = request.form['due_date']
        is_active = request.form['is_active']
        
        if(is_active=='1'):
            is_active = True
        elif(is_active=='0'):
            is_active = False

        new_serial = SerialsModel(ea_id=ea_id, user_id=user_id, broker_login=broker_login, s_key = s_key, is_active = is_active, due_date = due_date)
        db.session.add(new_serial)
        try:
            db.session.commit()
            info = flash("serial key created succefully!!!")
            return "serial key Added Successful"

        except sqlalchemy.exc.IntegrityError:
            return "Broker account registered, please register with a new account"

    @login_required
    def delete(self):
        id = request.args['id']
        SerialsModel.query.filter_by(id=id).delete()
        info = flash("Serial Deleted succefully!!!")
        return "serial key deleted succefully"

    # @login_required
    def patch(self):
        user_id = request.form['user_id']
        ea_id = request.form['ea_id']
        broker_login = request.form['broker_login']
        s_key = request.form['s_key']
        status = request.form['is_active']
        serial_update = SerialsModel.query.filter_by(user_id=user_id).first()

        if(serial_update==None):
            
            if(status=='1'):
                is_active = 1
            elif(status=='0'):
                is_active = 0

            new_serial = SerialsModel(ea_id=ea_id, user_id=user_id, broker_login=broker_login, s_key = s_key, is_active = is_active)
            db.session.add(new_serial)
            
            try:
                db.session.commit()
                info = flash("serial key created succefully!!!")
                return "serial key Added Successful"

            except:
                return "Broker account registered, please register with a new account"

        else:
            if ea_id !='' or None:
                serial_update.ea_id = ea_id

            if user_id !='' or None:
                serial_update.user_id = user_id

            if broker_login !='' or None:
                serial_update.broker_login = broker_login

            if s_key !='' or None:
                serial_update.s_key = s_key

            if status !='' or None:
                if status=='1':
                    serial_update.is_active = 1
                elif status=='0':
                    serial_update.is_active = 0
            db.session.commit()
            return {'msg': 'Update Successful'}
