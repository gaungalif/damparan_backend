# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, make_response, session, jsonify, redirect, url_for
# from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from apps import db
import uuid



from jinja2 import TemplateNotFound
from flask_cors import cross_origin

from apps.home.models import User

secret_key = "D4mP4R4n@123"

def login_required(f):
    """
    login required hanya untuk user biasa
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        # if "x-access-token" in request.headers:
            # token = request.headers['x-access-token']
        if session.get('token'):
            token = session.get('token')
        # return 401 if token is not passed
        if not token:
            return jsonify({'message':'token tidak ada, silakan login'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = User.query \
                .filter_by(employee_id=data['employee_id']) \
                .first()
        except:
            return jsonify({
                 'message': 'Token tidak cocok'
            }), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated

def moderator_required(f):
    """
    moderator required untuk user dengan moderator True
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        # if "x-access-token" in request.headers:
        #     token = request.headers['x-access-token']
        if session.get('token'):
            token = session.get('token')
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
            #return redirect(url_for('login'))

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = User.query \
                .filter_by(employee_id=data['employee_id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        # current_user.moderator = True
        if current_user.moderator:
            # returns the current logged in users context to the routes
            return f(current_user, *args, **kwargs)
        else:
            return jsonify({
                "message": "You are not moderator, action is not allowed"
            }), 403

    return decorated


def super_admin_required(f):
    """
    moderator required untuk user dengan moderator True
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        # if "x-access-token" in request.headers:
        #     token = request.headers['x-access-token']
        if session.get('token'):
            token = session.get('token')
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
            #return redirect(url_for('login'))

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = User.query \
                .filter_by(employee_id=data['employee_id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        if current_user.super_admin:
            # returns the current logged in users context to the routes
            return f(current_user, *args, **kwargs)
        else:
            return jsonify({
                "message": "You are not super admin, action is not allowed"
            }), 403

    return decorated

@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    # creates dictionary of form data
    if request.method == "POST":
        auth = request.json

        if not auth or not auth.get('email') or not auth.get('password'):
            # returns 401 if any email or / and password is missing
            return make_response({"status": "email dan password harus diisi"}, 401)

        user = User.query \
            .filter_by(email=auth.get('email')) \
            .first()

        if not user:
            # returns 401 if user does not exist
            return make_response({"status":"User email tidak ditemukan"}, 401)

        if check_password_hash(user.password, auth.get('password')):
            # generates the JWT Token
            token = jwt.encode({
                'employee_id': user.employee_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, secret_key)
            session['token'] = token
            return jsonify({'token': token})
        # returns 403 if password is wrong
        return jsonify({"status": "password salah"}, 403)
    else:
        return jsonify({"status": "silakan login"}, 200)
    
@blueprint.route('/logout')
@login_required
def logout(current_user):
    session.pop('user_id', None)
    session.pop('token', None)
    return redirect(url_for('home.login'))

@blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.json

    first_name, last_name, email = data.get('first_name'), data.get('first_name'), data.get('email')
    password = data.get('password')

    user = User.query \
        .filter_by(email=email) \
        .first()
    if not user:
        # database ORM object
        user = User(
            employee_id=str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password)
        )
        # insert user
        db.session.add(user)
        db.session.commit()

        return jsonify({"status": "Success"}, 200)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)


@blueprint.route('/')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@login_required
def index(current_user):
    return render_template('home/index.html', segment='index', current_user=current_user)
