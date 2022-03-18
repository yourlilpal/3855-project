import sqlite3

conn = sqlite3.connect('stats.sqlite')

c = conn.cursor()
c.execute(''' 
          CREATE TABLE stats 
          (id INTEGER PRIMARY KEY ASC,  
           num_of_name INTEGER NOT NULL, 
           num_of_password INTEGER NOT NULL,
           max_length_password INTEGER NOT NULL, 
           trace_id VARCHAR(20),  
           last_updated VARCHAR(100) NOT NULL) 
          ''')
conn.commit()
conn.close()
