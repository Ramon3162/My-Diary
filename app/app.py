from flask import Flask, jsonify, abort, request
from flask_jwt_extended import get_jwt_identity, jwt_required, JWTManager
from flask_bcrypt import Bcrypt
from app.models import theDatabase
from instance.config import app_config

    
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config['development'])
app.config.from_pyfile('config.py')

app.config['JWT_SECRET_KEY'] = 'yoursecretsaresafewithme'
jwt = JWTManager(app)


bcrypt = Bcrypt(app)


@app.route('/api/v1/entries', methods=['GET', 'POST'])
@jwt_required

def entries():
    if request.method == 'GET':
                
        """Gets all the entries by the user"""
        


        theDatabase().create_entry_table()
        return theDatabase().get_all_entries()

    else:
        #POST
        """Creates a single entry"""
        
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

@app.route('/api/v1/entries/<int:entry_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required

def manipulate_entries(entry_id):

    if request.method == 'GET':
    
        """Gets a single entry from the user"""

        theDatabase().create_entry_table()
        return theDatabase().get_one_entry(entry_id)

    elif request.method == 'PUT':

        """Updates a single entry"""

        title = request.json['title']
        description = request.json['description']
        
        entry_data = {
            'title' : title,
            'description' : description
        }

        theDatabase().create_entry_table()
        return theDatabase().update_entry(entry_id, entry_data)

    else:
        # DELETE
        """Deletes a single entry"""
        
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
  