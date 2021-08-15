from lucas_app import db, ma
from flask_restful import Resource
from .models import UsersModel
from werkzeug.utils import secure_filename
from flask import redirect, request, current_app as app, flash, url_for, jsonify
import os, uuid


class userSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsersModel
        fields = ['id', 'full_name', 'email', 'is_active', 'phone', 'description', 'password', 'photo', 'dob', 'added_on']

class UserResource(Resource):

    def get(self):
        
        try:
            email = request.args['email']
            get_user = UsersModel.query.filter_by(email = email).all()
        except:
            get_user = UsersModel.query.all()
        user_schema = userSchema(many=True)
        output = user_schema.dump(get_user)
        return output


    def post(self):
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        # try:
        #     photo = request.files['photo']
        #     if len(photo.filefull_name) != 0:
        #         photo_name = secure_filename(full_name + '.' + photo.filename.split('.')[-1])
        #     else:
        #         photo_name = ''
        #     product_photo_dir = os.path.join(app.config['IMAGE_UPLOADS'], 'users')
        #     photo.save(os.path.join(product_photo_dir, photo_name))
        # except:
        #     photo_name = ''

        new_user = UsersModel(full_name=full_name, phone = phone, email = email)
        db.session.add(new_user)
        db.session.commit()

        info = flash("user created succefully!!!")
        return "user Added Successful"

    def delete(self):
        id = request.args['id']
        UsersModel.query.filter_by(id=id).delete()
        info = flash("user Deleted succefully!!!")
        return "user deleted succefully"

    # TODO: FIX THE PHOTO UPDATE FEATURE
    def patch(self):

        id = request.form['id']
        user_update = UsersModel.query.filter_by(id=id).first()
        
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        status = request.form['status']
       

        if full_name !='' or None:
            user_update.full_name = full_name

        if email !='' or None:
            user_update.email = email

        if phone !='' or None:
            user_update.phone = phone 
        
        if status !='' or None:
            if status=='1':
                user_update.is_active = 1
            elif status=='0':
                user_update.is_active = 0
        db.session.commit()
        return {'msg': 'Update Successful'}
        
