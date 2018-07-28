from flask import Flask, jsonify, abort, request
from flask_jwt_extended import get_jwt_identity, jwt_required, JWTManager
from flask_bcrypt import Bcrypt
from app.models import theDatabase


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'yoursecretsaresafewithme'
jwt = JWTManager(app)


bcrypt = Bcrypt(app)


@app.route('/api/v1/entries', methods=['GET'])
@jwt_required

def get_all_entries():
    """Gets all the entries by the user"""
    
    # current_user = get_jwt_identity()

    theDatabase().create_entry_table()
    return theDatabase().get_all_entries()


@app.route('/api/v1/entries/<int:entry_id>', methods=['GET'])
@jwt_required

def get_single_entry(entry_id):
    """Gets a single entry from the user"""
    # current_user = get_jwt_identity()

    theDatabase().create_entry_table()
    return theDatabase().get_one_entry(entry_id)


@app.route('/api/v1/entries', methods=['POST'])
@jwt_required

def create_entry():
    """Creates a single entry"""
    
    # current_user = get_jwt_identity()
    if not request.json:
        abort(400)
    elif not 'title' in request.json:
        return jsonify({'message' : 'Title is required'}), 400
    elif not 'description' in request.json:
        return jsonify({'message' : 'Description is required'}), 400

    title = request.json['title']
    description = request.json['description']
    
    entry_data = {
        'title' : title,
        'description' : description
    }

    theDatabase().create_entry_table()
    return theDatabase().add_entry(entry_data)

@app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
@jwt_required

def update_entry(entry_id):
    """Updates a single entry"""

    # current_user = get_jwt_identity()
    title = request.json['title']
    description = request.json['description']
    
    entry_data = {
        'title' : title,
        'description' : description
    }

    theDatabase().create_entry_table()
    return theDatabase().update_entry(entry_id, entry_data)

@app.route('/api/v1/entries/<int:entry_id>', methods=['DELETE'])
@jwt_required

def delete_entry(entry_id):
    """Deletes a single entry"""

    # current_user = get_jwt_identity()
    
    theDatabase().create_entry_table()
    return theDatabase().delete_entry(entry_id)
    
@app.route('/auth/signup', methods=['POST'])
def signup():
    """Creates a user"""

    if not request.json:
        abort(400)
    elif not 'username' in request.json:
        return jsonify({'message' : 'Username is required'}), 400
    elif not 'email' in request.json:
        return jsonify({'message' : 'Email is required'}), 400
    elif not 'password' in request.json:
        return jsonify({'message' : 'Password is required'}), 401

    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')
  
    
    user_data = {
        'username': username,
        'password': hashed_password,
        'email': email,         
    }

    
    theDatabase().create_user_table()
    return theDatabase().signup(user_data)


@app.route('/auth/login', methods=['POST'])
def login():
    """Logs a user into the system"""
    
    if not request.json:
        abort(400)
    elif not 'username' in request.json:
        return jsonify({'message' : 'Username is required'}), 400
    elif not 'password' in request.json:
        return jsonify({'message' : 'Password is required'}), 401

    username = request.json['username']
    password = request.json['password']

    theDatabase().create_user_table()   
    return theDatabase().login(password, username)
   