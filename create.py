import sqlite3

conn = sqlite3.connect("bs.db")

c = conn.cursor()

q = "create table users(name text, age integer, id integer)"
c.execute(q)

q = "create table posts(name text, grade integer, id integer)"
c.execute(q)

#q = "create table messages(name text, grade integer, id integer)"
#c.execute(q)

q = "create table items(name text, price integer, id integer)"
c.execute(q)

conn.commit()
