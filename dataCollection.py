import sqlite3

connection = sqlite3.connect('collectedData.db')
cursor = connection.cursor()

cmd3 = """CREATE TABLE IF NOT EXISTS DATA(satisfaction boolean,
                                          quiz_attemps INTEGER DEFAULT 0)"""

cursor.execute(cmd3)

cmd4 = """INSERT INTO DATA(satisfaction, bike) values
                ('True', 'testing')"""
cursor.execute(cmd4)

connection.commit()

ans = cursor.execute("select * from DATA").fetchall()

for i in ans:
    print(i)