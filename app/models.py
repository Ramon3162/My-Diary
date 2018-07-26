from flask import jsonify, request
import psycopg2
from pprint import pprint

class theDatabase(object):

    def __init__(self):
        try:
            self.conn = psycopg2.connect("dbname='mydiary' host='localhost' user='postgres' password='3162' port='5432'")
            self.cursor = self.conn.cursor()
        except:
            pprint('Not connected')

    def create_table(self):
        self.cursor.execute("CREATE TABLE diary_users(user_id serial PRIMARY KEY, username varchar(30) NOT NULL, email varchar(30) NOT NULL, password varchar(50) NOT NULL)")
        self.conn.commit()

    def signup(self, user_data):
        """Create a new user in the database"""
        data1 = request.get_json()
        username = (data1['username'])
        
        self.cursor.execute("SELECT username FROM diary_users WHERE username = %s", (username, ))
        data = self.cursor.fetchall()
        if data:
            return jsonify({'message' : 'Username already exists'})
        else:
            self.cursor.execute("""INSERT INTO diary_users (username, password, email)
                                VALUES (%(username)s, %(password)s, %(email)s)""", user_data)
            self.conn.commit()
            return jsonify({'message' : 'User created successfully'})
 
    def login(self, username, password):
        """User login"""

        data1 = request.get_json()
        password = (data1['password'])
        username = (data1['username'])

        self.cursor.execute("""SELECT username FROM diary_users WHERE username = %s""", (username, ))
        data = self.cursor.fetchall()
        if data:
            self.cursor.execute("""SELECT password FROM diary_users WHERE password = %s""", (password, ))
            self.cursor.fetchall()
            return jsonify({'message':'Login successful'})
        else:
            return jsonify({'message':'Password is invalid'})
            