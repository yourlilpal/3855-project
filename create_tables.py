import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE password_user
          (id INTEGER PRIMARY KEY ASC, 
           user_id INTEGER NOT NULL,
           email VARCHAR(100) NOT NULL,
           name VARCHAR(100) NOT NULL,
           password VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE user_password
          (id INTEGER PRIMARY KEY ASC, 
           password_id VARCHAR(100) NOT NULL,
           password VARCHAR(100) NOT NULL,
           password_hint VARCHAR(100) NOT NULL,
           description VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
