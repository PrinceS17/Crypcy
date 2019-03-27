import sqlite3

conn = sqlite3.connect('proj.db')

print ("Opened database successfully");
#conn.execute('''DROP TABLE Currencies''')

conn.execute('''

         CREATE TABLE Currencies
         (CurrencyID TEXT PRIMARY KEY     NOT NULL,
         Name TEXT  NOT NULL,
         Logo BLOB  NOT NULL);''')



conn.execute(
         #DROP TABLE IF EXISTS User;
         '''CREATE TABLE User
         (UserID TEXT PRIMARY KEY     NOT NULL,
         Name TEXT  NOT NULL,
         Password TEXT  NOT NULL,
         Gender TEXT,
         Score_of_Knowledge TEXT,
         Interest_Tag TEXT);''')



print ("Table created successfully");

conn.commit();
conn.close();
#conn.close();
