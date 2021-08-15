from lucas_app import db, ma
from flask_restful import Resource
from .models import EAModel
from werkzeug.utils import secure_filename
from flask import redirect, request, current_app as app, flash, url_for, jsonify
import os, uuid


class eaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EAModel
        fields = ['id', 'name', 'description', 'summary', 'photo', 'added_on']

class EAResource(Resource):

    def get(self):
        try:
            id = request.args['id']
            get_book = EAModel.query.filter_by(id = id).all()
        except:
            get_book = EAModel.query.all()
        book_schema = eaSchema(many=True)
        output = book_schema.dump(get_book)
        return {'EAs': output}


    def post(self):
        name = request.form['name']
        description = request.form['description']
        try:
            photo = request.files['photo']
            if len(photo.filename) != 0:
                photo_name = secure_filename(name + '.' + photo.filename.split('.')[-1])
            else:
                photo_name = ''
            product_photo_dir = os.path.join(app.config['IMAGE_UPLOADS'], 'expert_advisors')
            photo.save(os.path.join(product_photo_dir, photo_name))
        except:
            photo_name = ''

        new_book = EAModel(name=name, description = description, photo = photo_name)
        db.session.add(new_book)
        db.session.commit()

        info = flash("Expert Advisor added succefully!!!")
        return "Expert Advisor Added Successful"

    def delete(self):
        id = request.args['id']
        EAModel.query.filter_by(id=id).delete()
        info = flash("Expert Advisor Deleted succefully!!!")
        return "Expert Advisor deleted succefully"

    # TODO: FIX THE PHOTO UPDATE FEATURE
    def patch(self):

        id = request.form['id']
        ea_update = EAModel.query.filter_by(id=id).first()
        
        name = request.form['name']
        description = request.form['description']
        summary = request.form['summary']
       

        if name !='' or None:
            ea_update.name = name

        if summary !='' or None:
            ea_update.summary = summary

        if description !='' or None:
            ea_update.description = description

        db.session.commit()
        return {'msg': 'Update Successful'}
        
