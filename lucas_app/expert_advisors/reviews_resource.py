from lucas_app import db, ma
from flask_restful import Resource
from .models import ReviewsModel
from werkzeug.utils import secure_filename
from flask import redirect, request, current_app as app, flash, url_for, jsonify
import os, uuid


class reviewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ReviewsModel
        fields = ['id', 'book_id', 'user_id', 'rating', 'comment_body', 'added_on']

class ReviewResource(Resource):

    def get(self):
        try:
            id = request.args['id']
            get_review = ReviewsModel.query.filter_by(id = id).all()
        except:
            get_review = ReviewsModel.query.all()
        review_schema = reviewsSchema(many=True)
        output = review_schema.dump(get_review)
        return {'review': output}


    def post(self):
        book_id = request.form['book_id']
        user_id = request.form['user_id']
        rating = request.form['rating']
        comment_body = request.form['comment_body']

        new_review = ReviewsModel(book_id=book_id, user_id = user_id, rating = rating, comment_body=comment_body)
        db.session.add(new_review)
        db.session.commit()

        info = flash("review created succefully!!!")
        return "review Added Successful"

    def delete(self):
        id = request.args['id']
        ReviewsModel.query.filter_by(id=id).delete()
        info = flash("review Deleted succefully!!!")
        return "review deleted succefully"

    def patch(self):

        id = request.form['id']
        review_update = ReviewsModel.query.filter_by(id=id).first()
        rating = request.form['rating']
        comment_body = request.form['comment_body']

        
        if rating !='' or None:
            review_update.rating = rating

        if comment_body !='' or None:
            review_update.comment_body = comment_body

        db.session.commit()
        return {'msg': 'Update Successful'}
