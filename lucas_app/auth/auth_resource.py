from lucas_app import db, ma, mail
from flask_restful import Resource
from ..users.models import UsersModel
from ..expert_advisors.models import SerialsModel
from werkzeug.utils import secure_filename
from flask import redirect, request, current_app as app, render_template, url_for
import os, uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_mail import Mail, Message
from flask_login import login_user, logout_user, current_user, login_manager
from . import auth


class userSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsersModel
        fields = ['id', 'full_name', 'email', 'phone', 'is_admin', 'is_active', 'password', 'photo', 'dob', 'added_on']

class AuthResource(Resource):

    def get(self):
        try:
            id = request.args['id']
            get_user = UsersModel.query.filter_by(id = id).all()
        except:
            get_user = UsersModel.query.all()
        user_schema = userSchema(many=True)
        output = user_schema.dump(get_user)
        return {'user': output}


    def post(self):
        full_name = request.form['full_name']
        is_admin = False
        is_active = True
        email = request.form['email']
        phone = request.form['phone']
        password = generate_password_hash(request.form['password'], method='sha256')
        confirm_code = generate_password_hash(str(datetime.now()), method='sha256')
        dob = request.form['dob']
        try:
            photo = request.files['photo']
            if len(photo.filefull_name) != 0:
                photo_name = secure_filename(full_name + '.' + photo.filename.split('.')[-1])
            else:
                photo_name = ''
            product_photo_dir = os.path.join(app.config['IMAGE_UPLOADS'], 'users')
            photo.save(os.path.join(product_photo_dir, photo_name))
        except:
            photo_name = ''

        new_user = UsersModel(full_name=full_name, password=password, confirm_code=confirm_code, phone = phone, dob=dob, is_admin = is_admin, is_active = is_active, email = email, photo = photo_name)
        db.session.add(new_user)
        db.session.commit()
        # TODO: SEND A CONFIRMATION LINK TO THE NEW USER ON REGISTRATION
        msg = Message(subject = 'lucas_app Account Confirmation', sender='dikeleon@gmail.com', recipients=[email])
        msg.html = render_template('auth/confirm_acc.html', email = email, confirm_code = confirm_code, full_name = full_name )
        mail.send(msg)
        return "Registration Successful"

    def delete(self):
        id = request.args['id']
        UsersModel.query.filter_by(id=id).delete()
        return "user deleted succefully"

    # TODO: FIX THE PHOTO UPDATE FEATURE
    def patch(self):

        id = request.form['id']
        user_update = UsersModel.query.filter_by(id=id).first()
        
        full_name = request.form['full_name']
        is_active = request.form['is_active']
        is_admin = request.form['is_admin']
        email = request.form['email']
       

        if full_name !='' or None:
            user_update.full_name = full_name

        if email !='' or None:
            user_update.email = email

        if is_active !='' or None:
            user_update.is_active = is_active

        if is_admin !='' or None:
            user_update.is_admin = is_admin

        db.session.commit()
        return {'msg': 'Update Successful'}
        

def confirm_account():
	email = request.args.get('email')
	confirm_code = request.args.get('confirm_code')
	db.session.query(UsersModel).filter(UsersModel.email == email).update({UsersModel.confirm_code:None}, synchronize_session = False)
	db.session.commit()
	return {'success': "Account Successfully confirmed, you can now login"}

# auth.route('/login', methods=['GET'])
def login_account():
    email = request.form['email']
    password = request.form['password']
    user = UsersModel.query.filter_by(email=email).first()
    if user:
        if user.check_password(password=password):
            if user.confirm_code != None:
                message = "confirm your email address please before attempting to login"
                return render_template('auth/login.html',message=message)
            login_user(user)
            if(user.is_admin):
                return redirect(url_for('admin.admin_index'))
            return redirect(url_for('users.user_cp_index'))
        else:
            message = "Incorrect Password!!!"
            return render_template('auth/login.html',message=message)
    message = "Please use a registered email"
    return render_template('auth/login.html',message=message)

def logout_account():
    logout_user()
    message = 'Logout Successful!!!'
    return render_template('auth/login.html',message=message)

# TODO MAKE A PASSWORD RESET FUNCTION
def reset_login():
    pass


# def check_serial():
#     return 'check serial'

@auth.route('/check_serial/', methods = ['POST','GET'])
def auth_serial():
    if request.method == "POST":
        ea_account_num = request.args.get('Login')
        ea_serial_key = request.args.get('Skey')
        try:
            auth_user = db.session.query(SerialsModel).filter(SerialsModel.broker_login == ea_account_num).filter(SerialsModel.s_key == ea_serial_key).filter(SerialsModel.is_active == 1).one()
            return "True", 200
        except:
            return "False", 404
    return "False", 404

