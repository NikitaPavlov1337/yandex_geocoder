import sqlite3 as sq
import csv


with sq.connect('out/ac_address.db') as con:
    cur = con.cursor()

    cur.execute(""" CREATE TABLE IF NOT EXISTS ac_address(
        lat REAL,
        lon REAL,
        country TEXT,
        subject TEXT,
        city TEXT,
        street TEXT,
        house TEXT
        )
        """)

a_file = open('out/new_output11.csv')
rows = csv.reader(a_file)
cur.executemany("INSERT INTO ac_address VALUES (?,?,?,?,?,?,?)",rows)

cur.execute("SELECT * FROM ac_address")
print(cur.fetchall())
con.commit()
con.close()