import sqlite3

conn = sqlite3.connect("bs.db")

c = conn.cursor()

q = "create table users(username text, password text, id integer)"
c.execute(q)

q = "create table posts(words text, id integer)"
c.execute(q)

#q = "create table messages(message text, grade integer, id integer)"
#c.execute(q)

q = "create table items(name text, price real, condition integer, category text, description text, id integer)"
c.execute(q)

conn.commit()
