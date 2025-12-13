import sqlite3

connection = sqlite3.connect('CollectedData.db')
cursor = connection.cursor()

cmd3 = """CREATE TABLE IF NOT EXISTS DATA(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            fisch_one varchar(5),
                                            fisch_two varchar(5),
                                            fisch_three varchar(5),
                                            fisch_four varchar(5),
                                            fisch_five varchar(50))"""

cursor.execute(cmd3)

cmd4 = """INSERT INTO DATA(fisch_one, fisch_two, fisch_three, fisch_four, fisch_five) values
                ('True', 'True', 'True', 'True', 'True')"""
cursor.execute(cmd4)

connection.commit()

ans = cursor.execute("select * from DATA").fetchall()

for i in ans:
    print(i)