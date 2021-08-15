from lucas_app import db, ma
from flask_restful import Resource
from .models import EAModel
from werkzeug.utils import secure_filename
from flask import redirect, request, current_app as app, flash, url_for, jsonify
import os, uuid
# from . import books


class bookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # model = EAModel
        fields = ['id', 'user_id', 'title', 'body', 'c_summary', 'added_on']

# class chapterSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = ChapterModel
#         fields = ['id', 'book_id', 'title', 'body', 'summary', 'added_on']
#         chaptersNested = ma.Nested(bookSchema, many=True)

# class BookResource(Resource):
# @books.route('/gt_misc_bks', methods=['GET'])
# def get_books():
#     try:
#         id = request.args['id']
#         get_book = db.session.query(EAModel.id, EAModel.user_id, ChapterModel.title, ChapterModel.summary.label('c_summary'), ChapterModel.body).filter_by(id = id).outerjoin(ChapterModel, EAModel.id==ChapterModel.book_id).all()
        
#     except:
#         get_book = EAModel.query.all()
#     book_schema = bookSchema(many=True)
#     output = book_schema.dump(get_book)
  
#     return {'book': output}


    
        
