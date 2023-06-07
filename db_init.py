import sqlite3

conn = sqlite3.connect('test.db')

conn.execute('''DROP TABLE MOVIES''')

conn.execute('''CREATE TABLE MOVIES
         (
         ID             INTEGER PRIMARY KEY AUTOINCREMENT,
         TITLE          TEXT    NOT NULL,
         DESCRIPTION    TEXT     NOT NULL,
         RELEASE_YEAR   INT CHECK ( RELEASE_YEAR>=1888 )
         );''')

# 1888 -> Louis Le Prince's Roundhay Garden Scene.

conn.execute("INSERT INTO MOVIES (ID,TITLE,DESCRIPTION,RELEASE_YEAR) \
      VALUES (1, 'The Matrix', 'The Matrix is a computer-generated gream world...', 1999 );")

conn.execute("INSERT INTO MOVIES (ID,TITLE,DESCRIPTION,RELEASE_YEAR) \
      VALUES (2, 'The Matrix Reloaded', 'Continuation of the cult classic The Matrix...', 2003 );")

conn.execute("INSERT INTO MOVIES (ID,TITLE,DESCRIPTION,RELEASE_YEAR) \
      VALUES (3, 'Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster...', 1994 );")

conn.execute("INSERT INTO MOVIES (ID,TITLE,DESCRIPTION,RELEASE_YEAR) \
      VALUES (4, 'Drive', 'A mysterious Hollywood action film stuntman gets in trouble...', 2011 );")

conn.execute("INSERT INTO MOVIES (ID,TITLE,DESCRIPTION,RELEASE_YEAR) \
      VALUES (5, 'Kung Fury', 'Kung Fury, the toughest martial artist cop goes back in time...', 2015 );")


print("Database ready.")
conn.commit()
conn.close()