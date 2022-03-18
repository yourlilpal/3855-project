import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE "user_password"
          ''')
c.execute('''
          DROP TABLE "password_user"
          ''')
conn.commit()
conn.close()
