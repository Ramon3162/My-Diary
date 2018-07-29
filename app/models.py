from flask import Flask, jsonify, request
import psycopg2
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token)
from datetime import timedelta
from instance.config import app_config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config['development'])
app.config.from_pyfile('config.py')

app.config['JWT_SECRET_KEY'] = 'yoursecretsaresafewithme'
jwt = JWTManager(app)

bcrypt = Bcrypt(app)


class theDatabase(object):

    def __init__(self):
        self.conn = psycopg2.connect("dbname='mydiary' host='localhost' user='postgres' password='3162' port='5432'")
        self.cursor = self.conn.cursor()

    def create_user_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS diary_users(
                            user_id SERIAL PRIMARY KEY, 
                            username varchar(30) NOT NULL,
                            email varchar(30) NOT NULL,
                            password varchar(150) NOT NULL)""")
        self.conn.commit()

    def create_entry_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS diary_entries(
                            entry_id SERIAL,
                            entry_title varchar(50) NOT NULL,
                            description varchar(300) NOT NULL)""")
        self.conn.commit()

    def drop_entry_table(self):
        self.cursor.execute("""DROP TABLE diary_entries""")
        self.conn.commit()
    
    def drop_user_table(self):
        self.cursor.execute("""DROP TABLE diary_users""")
        self.conn.commit()

    def signup(self, user_data):
        """Create a new user in the database"""
        User = request.get_json()
        username = (User['username'])
        
        self.cursor.execute("SELECT username FROM diary_users WHERE username = %s", (username, ))
        username_data = self.cursor.fetchall()
        if not username_data:
            self.cursor.execute("""INSERT INTO diary_users (username, password, email)
                                VALUES (%(username)s, %(password)s, %(email)s)""", user_data)
            self.conn.commit()
            return jsonify({'message' : 'User created successfully'}), 201
        else:
            return jsonify({'message' : 'Username already exists'}), 400
            
 
    def login(self, username, password):
        """User login"""

        credentials = request.get_json()
        password = (credentials['password'])
        username = (credentials['username'])

        self.cursor.execute("""SELECT password FROM diary_users WHERE username = %s""", (username, ))
        data = self.cursor.fetchone()
        if data:
            if bcrypt.check_password_hash(data[0], password):
                expiration = timedelta(minutes=30)
                access_token = create_access_token(identity=username, expires_delta=expiration)
                return jsonify({'token' : access_token,'message':'Login successfull' }), 200
            else:
                return jsonify({'message':'Password is invalid'}), 400
        else:
            return jsonify({'message' : 'Username is invalid'}), 400

    def add_entry(self, entry_data):
        """Adds new entry to tha database"""

        self.cursor.execute("""INSERT INTO diary_entries (entry_title, description) VALUES (%(title)s, %(description)s)""", entry_data)
        self.conn.commit()
        return jsonify({'message' : 'Entry created successfully'}), 200

    def get_one_entry(self, entry_id):
        """Allows for viewing of one diary entry"""
        
        self.cursor.execute("""SELECT * FROM diary_entries WHERE entry_id = %s""", (entry_id, ))
        data = self.cursor.fetchall()
        if data:
            return jsonify({'Entry' : data, 'message' : 'Entry retrieved successfully'}), 200
        else:
            return jsonify({'message' : 'Entry not found'})

    def get_all_entries(self):
        """Allows for the viewing of all the diary entries of a user"""

        self.cursor.execute("""SELECT * FROM diary_entries""")
        data = self.cursor.fetchall()
        if data:
            return jsonify({'Entries' : data, 'message' : 'All entries found successfully'})
        else:
            return jsonify({'message': 'No entries found'})

    def update_entry(self, entry_id, entry_data):
        """Allows for the updating of a single diary entry"""

        self.cursor.execute("""SELECT * FROM diary_entries WHERE entry_id = %s""", (entry_id, ))
        data = self.cursor.fetchall()
        if data:
            self.cursor.execute("""UPDATE diary_entries set entry_title=%(title)s, description=%(description)s """, entry_data)
            self.conn.commit()
            self.cursor.execute("""SELECT * FROM diary_entries WHERE entry_id = %s""", (entry_id, ))
            updated_data = self.cursor.fetchall()
            return jsonify({'Entry' : updated_data, 'message' : 'Entry updated successfully'}), 200
        else:
            return jsonify({'message' : 'Entry not found'})

    def delete_entry(self, entry_id):
        """Allows for the deletion of one diary entry"""

        self.cursor.execute("""DELETE FROM diary_entries WHERE entry_id = %s""", (entry_id,))
        self.conn.commit()
        return jsonify({'message' : 'Entry deleted successfully'})
            