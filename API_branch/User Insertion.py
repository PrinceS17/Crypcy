import sqlite3

conn=sqlite3.connect('proj.db')
userid=[];
name=[];
gender=[];
password=[];
score_of_knowledge=[];
interest_tag=[];
for i in range(10):
    userid.append('0'+str(i));

for i in range(10):
    if(i%2==0):
        gender.append('Male');
    else:
        gender.append('Female');

for i in range(10):
    if(i%2==0):
        password.append('Abc123');
        interest_tag.append('Bitcoin');
    else:
        password.append('Def456');
        interest_tag.append('EOS')

name.append('Sam');
name.append('Lily');
name.append('Bill');
name.append('Betty');
name.append('Jack');
name.append('Cindy');
name.append('Mike');
name.append('Alice');
name.append('Robert');
name.append('Helen');

for i in range(10):
    score_of_knowledge.append(str(5+i*10));
#for i in

for i in range(len(name)):
    ID=userid[i];
    NAME=name[i];
    PASSWORD=password[i];
    GENDER=gender[i];
    SCORE_OF_KNOWLEDGE=score_of_knowledge[i];
    INTEREST_TAG=interest_tag[i];

    conn.execute("INSERT OR REPLACE INTO User (UserID,Name,Password,Gender,Score_of_Knowledge,Interest_Tag) VALUES(?,?,?,?,?,?)",
    (ID,NAME,PASSWORD,GENDER,SCORE_OF_KNOWLEDGE,INTEREST_TAG))


conn.commit();
cursor = conn.cursor()
#cursor.execute("SELECT * FROM Currencies")
cursor.execute("SELECT * FROM User")
print(cursor.fetchall());
conn.close();
