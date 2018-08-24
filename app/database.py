"""Database handling"""
import os
import psycopg2


class Database:
    """Create the database class"""
    def __init__(self):
        dbname = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            host=host,
            password=password,
            port=port)
        self.cursor = self.conn.cursor()

    def create_user_table(self):
        """Creates table to hold user data"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS diary_users(
                            user_id SERIAL PRIMARY KEY, 
                            username varchar(30) NOT NULL,
                            email varchar(30) NOT NULL,
                            status varchar(30) NOT NULL,
                            password varchar(150) NOT NULL)""")
        self.cursor.close()
        self.conn.commit()

    def create_entry_table(self):
        """Creates table to hold entry data"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS diary_entries(
                            entry_id SERIAL,
                            id INTEGER,
                            entry_title varchar(50) NOT NULL,
                            description varchar(300) NOT NULL,
                            date_posted timestamp NOT NULL,
                            PRIMARY KEY(entry_id, id),
                            FOREIGN KEY(id) REFERENCES diary_users(user_id));""")
        self.cursor.close()
        self.conn.commit()

    def drop_entry_table(self):
        """Drop enntry table after tests"""
        self.cursor.execute("""DROP TABLE IF EXISTS diary_entries CASCADE""")
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def drop_user_table(self):
        """Drop user table after every test"""
        self.cursor.execute("""DROP TABLE IF EXISTS diary_users CASCADE""")
        self.cursor.close()
        self.conn.commit()
        self.conn.close()