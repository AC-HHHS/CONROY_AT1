import sqlite3

connection = sqlite3.connect('collectedData.db')
cursor = connection.cursor()

cmd3 = """CREATE TABLE IF NOT EXISTS DATA(fav_animal varchar(50),
                                          satisfaction boolean,
                                          bike varchar(50))"""

cursor.execute(cmd3)

cmd4 = """INSERT INTO DATA(fav_animal, satisfaction, bike) values
                ('exist','True', 'testing')"""
cursor.execute(cmd4)

connection.commit()

ans = cursor.execute("select * from DATA").fetchall()

for i in ans:
    print(i)