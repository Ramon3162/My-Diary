"""Models handling"""
import os
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from app.database import Database
from flask_jwt_extended import (
    JWTManager, create_access_token)

app = Flask(__name__, instance_relative_config=True)


app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
jwt = JWTManager(app)

bcrypt = Bcrypt(app)


class User(Database):
    """Create the User class"""
    def signup(self, user_data):
        """Create a new user in the database"""
        user = request.get_json()
        username = (user['username'])
        email = (user['email'])
        self.cursor.execute("SELECT email FROM diary_users WHERE email = %s", (email, ))
        email_data = self.cursor.fetchall()
        self.cursor.execute("SELECT username FROM diary_users WHERE username = %s", (username, ))
        username_data = self.cursor.fetchall()
        if not username_data:
            if not email_data:
                self.cursor.execute("""INSERT INTO diary_users (username, password, email, status)
                                    VALUES (%(username)s, %(password)s, %(email)s, %(status)s)""", user_data)
                self.conn.commit()
                self.cursor.execute("SELECT * FROM diary_users WHERE username = %s", (username, ))
                data = self.cursor.fetchone()
                return jsonify({'User': User().display_user(data), 'message' : 'User created successfully'}), 201
            return jsonify({'message' : 'Email already exists'}), 400
        return jsonify({'message' : 'Username already exists'}), 400
    
    def login(self, username, password):
        """User login"""
        credentials = request.get_json()
        password = (credentials['password'])
        username = (credentials['username'])

        self.cursor.execute("""SELECT password FROM diary_users WHERE username = %s""",
                            (username, ))
        data = self.cursor.fetchone()
        self.cursor.execute("""SELECT user_id FROM diary_users WHERE username = %s""",
                            (username, ))
        id_data = self.cursor.fetchone()
        if data:
            if bcrypt.check_password_hash(data[0], password):
                expiration = timedelta(minutes=30)
                access_token = create_access_token(identity=id_data, expires_delta=expiration)
                self.cursor.execute("SELECT * FROM diary_users WHERE username = %s", (username, ))
                data = self.cursor.fetchone()
                if data:
                    return jsonify({'token' : access_token, 'User' :User().display_user(data) , 'message':'Login successfull'}), 200
            return jsonify({'message':'Password is invalid'}), 400
        return jsonify({'message' : 'Username is invalid'}), 400

    def get_user_data(self, user_id):
        """Method to get user data"""
        self.cursor.execute("SELECT * FROM diary_users WHERE user_id = %s", (user_id, ))
        data = self.cursor.fetchone()
        if data:
            return jsonify({'User' : User().display_user(data), 'message' : 'User retrieved successfully'}), 200
        return jsonify({'message' : 'User not found'})
    
    def update_user_data(self, user_id, username, email, status):
        """Method to update user data"""
        self.cursor.execute("SELECT * FROM diary_users WHERE user_id = %s", (user_id, ))
        data = self.cursor.fetchone()
        if data:
            self.cursor.execute("""UPDATE diary_users set username = %s, email = %s,
                                status = %s WHERE user_id = %s""", (username, email, status, user_id, ))
            self.conn.commit()
            self.cursor.execute("""SELECT * FROM diary_users WHERE user_id = %s""",
                                (user_id, ))
            updated_data = self.cursor.fetchone()
            return jsonify({'User' : User().display_user(updated_data), 'message' : 'User data updated successfully'}), 200
        return jsonify({'message' : 'User not found'})


    def display_user(self,user):
        """Dictionary to hold entry data"""
        self.cursor.execute("""SELECT COUNT(entry_title) FROM diary_entries WHERE id = %s""", (user[0], ))
        entry_data = self.cursor.fetchone()
        return dict(
            user_id=user[0],
            username=user[1],
            email=user[2],
            status=user[3],
            entries=entry_data[0]
        )

class Entry(Database):
    """Class to handle entries"""
    def add_entry(self, current_user, title, description, date_posted):
        """Adds new entry to tha database"""
        self.cursor.execute("""SELECT * FROM diary_entries WHERE id = %s AND entry_title = %s""",
                            (current_user, title, ))
        result = self.cursor.fetchall()
        if result:
            return jsonify({'message' : 'You cannot publish a duplicate entry.'}), 400
        self.cursor.execute("""INSERT INTO diary_entries (id, entry_title, description, date_posted)
                            VALUES (%s, %s, %s, %s)""", (current_user, title, description, date_posted,))
        self.conn.commit()
        self.cursor.execute("""SELECT * FROM diary_entries WHERE id = %s AND entry_id = (SELECT MAX(entry_id) FROM diary_entries)""", (current_user,))
        data = self.cursor.fetchone()
        return jsonify({'Entry': Entry().display_entry(data), 'message' : 'Entry created successfully'}), 201
    def get_one_entry(self, entry_id, current_user):
        """Allows for viewing of one diary entry"""
        self.cursor.execute("""SELECT * FROM diary_entries WHERE entry_id = %s AND id = %s""",
                            (entry_id, current_user, ))
        data = self.cursor.fetchone()
        if data:
            return jsonify({'Entry' : Entry().display_entry(data), 'message' : 'Entry retrieved successfully'}), 200
        return jsonify({'message' : 'Entry not found'})

    def get_all_entries(self, current_user):
        """Allows for the viewing of all the diary entries of a user"""
        self.cursor.execute("""SELECT * FROM diary_entries WHERE id = %s""", (current_user,))
        data = self.cursor.fetchall()
        if data:
            return jsonify({'Entries' : [Entry().display_entry(entry) for entry in data], 'message' : 'All entries found successfully'})
        return jsonify({'message': 'No entries found'})

    def update_entry(self, entry_id, title, description, current_user):
        """Allows for the updating of a single diary entry"""

        self.cursor.execute("""SELECT * FROM diary_entries WHERE entry_id = %s AND id = %s""",
                            (entry_id, current_user, ))
        data = self.cursor.fetchall()
        if data:
            self.cursor.execute("""UPDATE diary_entries set entry_title = %s,
                                description = %s WHERE entry_id = %s""", (title, description, entry_id, ))
            self.conn.commit()
            self.cursor.execute("""SELECT * FROM diary_entries WHERE entry_id = %s""", (entry_id, ))
            updated_data = self.cursor.fetchone()
            return jsonify({'Entry' : Entry().display_entry(updated_data), 'message' : 'Entry updated successfully'}), 200
        return jsonify({'message' : 'Entry not found'})

    def delete_entry(self, entry_id, current_user):
        """Allows for the deletion of one diary entry"""

        self.cursor.execute("""SELECT * FROM diary_entries WHERE entry_id = %s AND id = %s""",
                            (entry_id, current_user, ))
        data = self.cursor.fetchall()
        if data:
            self.cursor.execute("""DELETE FROM diary_entries WHERE entry_id = %s""", (entry_id, ))
            self.conn.commit()
            return jsonify({'message' : 'Entry deleted successfully'}), 200
        return jsonify({'message' : 'Entry not found.'}), 400

    def display_entry(self,entry):
        """Dictionary to hold entry data"""
        return dict(
            id=entry[0],
            user_id=entry[1],
            title=entry[2],
            description=entry[3],
            date_posted=entry[4].strftime("%Y-%m-%d")
        )
            