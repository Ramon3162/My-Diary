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

    def create_user_table(self):
        self.cursor.execute("""CREATE TABLE diary_users(user_id serial PRIMARY KEY, 
                            username varchar(30) NOT NULL,
                            email varchar(30) NOT NULL,
                            password varchar(50) NOT NULL)""")
        self.conn.commit()

    def create_entry_table(self):
        self.cursor.execute("""CREATE TABLE diary_entries(entry_id serial PRIMARY KEY,
                            entry_title varchar(50) NOT NULL,
                            description varchar(300) NOT NULL)""")
        self.conn.commit()


    def signup(self, user_data):
        """Create a new user in the database"""
        User = request.get_json()
        username = (User['username'])
        
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

        credentials = request.get_json()
        password = (credentials['password'])
        username = (credentials['username'])

        self.cursor.execute("""SELECT username FROM diary_users WHERE username = %s""", (username, ))
        data = self.cursor.fetchall()
        if data:
            self.cursor.execute("""SELECT password FROM diary_users WHERE password = %s""", (password, ))
            self.cursor.fetchall()
            return jsonify({'message':'Login successful'})
        else:
            return jsonify({'message':'Password is invalid'})

    def add_entry(self, entry_data):
        """Adds new entry to tha database"""

        self.cursor.execute("""INSERT INTO diary_entries (entry_title, description) VALUES (%(title)s, %(description)s)""", entry_data)
        self.conn.commit()
        return jsonify({'message' : 'Entry created successfully'})

    def get_one_entry(self, entry_id):
        """Allows for viewing of one diary entry"""
        try:
            self.cursor.execute("""SELECT * FROM diary_entries WHERE entry_id = %s""", (entry_id, ))
            data = self.cursor.fetchall()
            return jsonify({'Entry' : data, 'message' : 'Entry retrieved successfully'})
        except:
            return jsonify({'message' : 'Entry not found'})

    def get_all_entries(self):
        """Allows for the viewing of all the diary entries of a user"""

        self.cursor.execute("""SELECT * FROM diary_entries""")
        data = self.cursor.fetchall()
        return jsonify({'Entries' : data, 'message' : 'All entries found successfully'})

    def update_entry(self, entry_id, entry_data):
        """Allows for the updating of a single diary entry"""

        self.cursor.execute("""SELECT * FROM diary_entries WHERE entry_id = %s""", (entry_id, ))
        data = self.cursor.fetchall()
        if data:
            self.cursor.execute("""UPDATE diary_entries set entry_title=%(title)s, description=%(description)s """, entry_data)
            self.conn.commit()
            self.cursor.execute("""SELECT * FROM diary_entries WHERE entry_id = %s""", (entry_id, ))
            updated_data = self.cursor.fetchall()
            return jsonify({'Entry' : updated_data, 'message' : 'Entry updated successfully'})
        else:
            return jsonify({'message' : 'Entry not found'})

    def delete_entry(self, entry_id):
        """Allows fro the deletion of one diary entry"""

        self.cursor.execute("""DELETE FROM diary_entries WHERE entry_id = %s""", (entry_id,))
        self.conn.commit()
        return jsonify({'message' : 'Entry deleted successfully'})
            