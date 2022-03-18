import mysql.connector

db_conn = mysql.connector.connect(host="kafka-3855.eastus2.cloudapp.azure.com", user="user",
                                  password="password", database="events")

db_cursor = db_conn.cursor()
db_cursor.execute('''
          CREATE TABLE password_user
          (id INT NOT NULL AUTO_INCREMENT, 
           user_id INTEGER NOT NULL,
           email VARCHAR(100) NOT NULL,
           name VARCHAR(100) NOT NULL,
           password VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           CONSTRAINT password_user_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE user_password
          (id INT NOT NULL AUTO_INCREMENT, 
           password_id VARCHAR(100) NOT NULL,
           password VARCHAR(100) NOT NULL,
           password_hint VARCHAR(100) NOT NULL,
           description VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           CONSTRAINT user_password_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()
