"""API routes"""
import re
import os
from datetime import datetime
from flask import Flask, jsonify, abort, request, render_template, make_response
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.models import User, Entry
from app.database import Database
# from app.validators import validate_entry_inputs
from instance.config import app_config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config[os.getenv('APP_SETTINGS')])
app.config.from_pyfile('config.py')

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
jwt = JWTManager(app)
CORS(app)
bcrypt = Bcrypt(app)

@app.route('/api/v1/entries', methods=['GET', 'POST'])
@jwt_required

def entries():
    """Method that handles posting an entry/retreiving of entries"""
    current_user = get_jwt_identity()[0]
    if request.method == 'GET':
        Database().create_entry_table()
        return Entry().get_all_entries(current_user)
    else:
        if not request.json:
            return jsonify({'message' : 'Error 400. Request needs to be in JSON format.'}), 400
        elif not 'title' in request.json:
            return jsonify({'message' : 'Title is required'}), 400
        elif not 'description' in request.json:
            return jsonify({'message' : 'Description is required'}), 400
        title = request.json['title']
        description = request.json['description']
        date_posted =datetime.utcnow().isoformat()
        if len(title.strip(" ")) < 1:
            return jsonify({'message' : 'Entry title cannot be empty.'}), 400
        elif len(description.strip(" ")) < 1:
            return jsonify({'message' : 'Entry description cannot be empty.'}), 400
        # validate_entry_inputs(request.json)
        # title = request.json['title']
        # description = request.json['description']
        # date_posted = datetime.utcnow().isoformat()
        Database().create_entry_table()
        return Entry().add_entry(current_user, title, description, date_posted)

@app.route('/api/v1/entries/<int:entry_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required

def manipulate_entries(entry_id):
    """Handling of specific entries"""
    current_user = get_jwt_identity()[0]
    if request.method == 'GET':
        Database().create_entry_table()
        return Entry().get_one_entry(entry_id, current_user)
    elif request.method == 'PUT':
        if not request.json:
            return jsonify({'message' : 'Error 400. Request needs to be in JSON format.'}), 400
        elif not 'title' in request.json:
            return jsonify({'message' : 'Title is required'}), 400
        elif not 'description' in request.json:
            return jsonify({'message' : 'Description is required'}), 400
        title = request.json['title']
        description = request.json['description']
        if len(title.strip(" ")) < 1:
            return jsonify({'message' : 'Entry title cannot be empty.'}), 400
        elif len(description.strip(" ")) < 1:
            return jsonify({'message' : 'Entry description cannot be empty.'}), 400

        # validate_entry_inputs(request.json)
        title = request.json['title']
        description = request.json['description']
        Database().create_entry_table()
        return Entry().update_entry(entry_id, title, description, current_user)
    else:
        Database().create_entry_table()
        return Entry().delete_entry(entry_id, current_user)

@app.route('/auth/signup', methods=['POST'])
def signup():
    """Creates a user"""
    if not request.json:
        return({'message' : 'Reaquest should be in json format'}), 400
    elif not 'username' in request.json:
        return jsonify({'message' : 'Username is required'}), 400
    elif not 'email' in request.json:
        return jsonify({'message' : 'Email is required'}), 400
    elif not 'password' in request.json:
        return jsonify({'message' : 'Password is required'}), 400
    elif not 'confirm_password' in request.json:
        return jsonify({'message' : 'Confirm password field is required'}), 400
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    confirm_password = request.json['confirm_password']
    hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')

    valid_email = re.compile(r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[.a-zA-Z-]+$)")
    valid_username = re.compile(r"(^[a-zA-Z0-9_.-]+$)")
    if not re.match(valid_username, username):
        return jsonify({'message' : 'Username should not have any special characters.'}), 400
    elif len(username) < 3:
        return jsonify({'message' : 'Username should be at least three characters long.'}), 400
    elif password != confirm_password:
        return jsonify({'message' : 'Passwords provided do not match.'}), 400
    elif len(password) < 8:
        return jsonify({'message' : 'Password should be at least eight characters long.'}), 400
    elif not re.match(valid_email, email):
        return jsonify({'message' : 'Invalid email format.'}), 400
    user_data = {
        'username': username,
        'password': hashed_password,
        'email': email,
        'status': 'Update your bio',
        }
    Database().create_user_table()
    return User().signup(user_data)

@app.route('/auth/login', methods=['POST'])
def login():
    """Logs a user into the system"""
    if not request.json:
        return jsonify({'message' : 'Error 400. Request needs to be in JSON format.'}), 400
    elif not 'username' in request.json:
        return jsonify({'message' : 'Username is required'}), 400
    elif not 'password' in request.json:
        return jsonify({'message' : 'Password is required'}), 401
    username = request.json['username']
    password = request.json['password']
    Database().create_user_table()
    return User().login(password, username)

@app.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required

def update_user(user_id):
    """Updates user data"""
    current_user = get_jwt_identity()[0]
    if not request.json:
        return jsonify({'message' : 'Error 400. Request needs to be in JSON format.'}), 400
    elif not 'username' in request.json:
        return jsonify({'message' : 'Username is required'}), 400
    elif not 'email' in request.json:
        return jsonify({'message' : 'Email is required'}), 400
    username = request.json['username']
    email = request.json['email']
    status = request.json['status']

    valid_email = re.compile(r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[.a-zA-Z-]+$)")
    valid_username = re.compile(r"(^[a-zA-Z0-9_.-]+$)")
    if not re.match(valid_username, username):
        return jsonify({'message' : 'Username should not have any special characters.'}), 400
    elif len(username) < 3:
        return jsonify({'message' : 'Username should be at least three characters long.'}), 400
    elif not re.match(valid_email, email):
        return jsonify({'message' : 'Invalid email format.'}), 400
    user_data = {
        'username': username,
        'email': email,
        'status': status,
        }
    Database().create_user_table()
    return User().update_user(user_data, current_user)


@app.errorhandler(404)
def entry_not_found(error):
    """404 Error Handler"""
    return make_response(jsonify({'Error': 'Invalid input'}), 404)

@app.errorhandler(500)
def server_error(error):
    """500 Error Handler"""
    return make_response(jsonify({'Error': 'Internal server error'}), 500)

@app.route("/")
def index():
    """Template to redirect to the documentation"""
    return render_template("documentation.html")
    