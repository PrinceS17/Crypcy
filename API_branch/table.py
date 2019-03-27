import sqlite3

conn = sqlite3.connect('proj.db')
#conn.execute('''DROP TABLE Currencies''')
# create table of Currencies
conn.execute('''

         CREATE TABLE IF NOT EXISTS Currencies
         (CurrencyID TEXT PRIMARY KEY     NOT NULL,
         Name TEXT  NOT NULL,
         Logo BLOB  NOT NULL);''')


# create table of User
conn.execute(

         '''CREATE TABLE IF NOT EXISTS User
         (UserID TEXT PRIMARY KEY     NOT NULL,
         Name TEXT  NOT NULL,
         Password TEXT  NOT NULL,
         Gender TEXT,
         Score_of_Knowledge TEXT,
         Interest_Tag TEXT);''')

#create table of Related_News
conn.execute(
         #DROP TABLE IF EXISTS User;
         '''CREATE TABLE IF NOT EXISTS Related_News
         (FactID TEXT PRIMARY KEY     NOT NULL,
         Tag TEXT,
         Type TEXT,
         Picture BLOB,
         Content TEXT,
         Author TEXT);''')

# create table of Timeslot
conn.execute(

         '''CREATE TABLE IF NOT EXISTS Timeslot
         (SlotID DATE PRIMARY KEY     NOT NULL,
         FactID TEXT,
         FOREIGN KEY (FactID) REFERENCES Related_News(FactID));''')

# create table of metric
conn.execute(
            ''' CREATE TABLE IF NOT EXISTS Metric
            (CurrencyID TEXT  NOT NULL,
            SlotID DATE    NOT NULL,
            Volume REAL NOT NULL,

            Price REAL  NOT NULL,
            Circulating_Supply REAL,
            Utility_Value REAL,
            FOREIGN KEY (CurrencyID) REFERENCES Currencies(CurrencyID),
            FOREIGN KEY (SlotID) REFERENCES Timeslot(SlotID),
            PRIMARY KEY (CurrencyID,SlotID));''')
#Privacy REAL,
print ("Table created successfully");

conn.commit();
conn.close();
#conn.close();
