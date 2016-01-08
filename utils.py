import sqlite3
import md5;
import re;
def sanitize(input):
    return re.sub('"', "  ", input)

def encrypt(username,password):
    m = md5.new()
    m.update(username+password)
    return m.hexdigest()
    #hashes and salts the pasword for permanent storage or retrieval
    #returns hashed password

def authenticate(username, password):
    username = sanitize(username)
    conn = sqlite3.connect("bs.db")
    c = conn.cursor()
    ans = c.execute('select * from users where username = "'+username+'" and password = "'+encrypt(username,password)+'";') 
    for r in ans:
        return True;
    return False;
    #returns a boolean that describes whether the user has succesfully logged in.

def newUser(username,password):
    username = sanitize(username)
    conn = sqlite3.connect("bs.db")
    c = conn.cursor()
    ans = c.execute('select * from users where username = "%s";' % username)
    for r in ans:
        return False
    ans = c.execute('insert into logins values("'+username+'","'+encrypt(username,password)+'");')
    conn.commit()
    return True

def changePassword(username, oldPassword, newPassword):
    newPassword = sanitize(newPassword);
    username = sanitize(username);
    if(authenticate(username,oldPassword)):
       conn = sqlite3.connect("bs.db")
       c = conn.cursor()
       c.execute('update users set password = "%s" where username = "%s";' % (encrypt(username,newPassword), username))
       conn.commit()
       return True
    return False

def getAllItems():
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from items;')
    return c.fetchall()

def getAllPosts():
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from posts;')
    return c.fetchall()

#search items
