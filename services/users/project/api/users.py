""" services/users/project/api/users.py """

from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project.api.models import User
from project import db
from project.api.utils import authenticate, is_admin

users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db.session.add(User(username=username, email=email, password=password))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/users', methods=['POST'])
@authenticate
def add_user(resp):
    post_data = request.get_json()
    response = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    if not is_admin(resp):
        response['message'] = 'You do not have permission to do that.'
        return jsonify(response), 401
    if not post_data:
        return jsonify(response), 400

    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            response['status'] = 'success'
            response['message'] = f'{email} was added!'
            return jsonify(response), 201
        else:
            response['message'] = 'Sorry, That email already exists.'
            return jsonify(response), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify(response), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user by id"""
    response = {
        'status': 'fail',
        'message': 'User does not exist.'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response), 404
        else:
            return jsonify({
                'status': 'success',
                'data': user.to_json()
            }), 200
    except ValueError:
        return jsonify(response), 404


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    response = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response), 200
