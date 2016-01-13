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
def countUserID():
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from users;')
    items = c.fetchall()
    n = 0
    for i in items:
        n = n + 1
    return n

def getUserID(username):
    conn = sqlite3.connect("bs.db")
    c = conn.cursor()
    q = "SELECT Username,UserID FROM users;"
    UserID = -1
    for i in c.execute(q):
        if i[0] == username:
            UserID = i[1]
    conn.commit()
    conn.close()
    return UserID

def newUser(username,password):
    username = sanitize(username)
    conn = sqlite3.connect("bs.db")
    c = conn.cursor()
    ans = c.execute('select * from users where username = "%s";' % username)
    for r in ans:
        return False
    ans = c.execute('insert into users values("'+username+'","'+encrypt(username,password)+'","'+str(countUserID() + 1)+'");')
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

def addItem(name, price, condition, category, description,user):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('insert into items values("'+name+'","'+str(price)+'","'+str(condition)+'","'+category+'","'+description+'","'+str(getItemID() + 1)+'","'+str(getUserID(user))+'")')
    conn.commit()

def addPost(title,content,user):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('insert into posts values("'+content+'","'+title+'","'+str(getPostID() + 1)+'","'+str(getUserID(user))+'")')
    conn.commit()

def getItemID():
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from items;')
    items = c.fetchall()
    n = 0
    for i in items:
        n = n + 1
    return n

def getPostID():
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from posts;')
    posts = c.fetchall()
    n = 0
    for p in posts:
        n = n + 1
    return n

def editPost(userID, postID, new_content):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    q = """
    UPDATE posts
    SET content='""" + new_content +"""'
    WHERE UserID='"""+ str(userID) + """'
    AND BlogID='"""+ str(postID) + """'
    """
    c.execute(q)
    conn.commit()
    conn.close()

#need to change Id after deleting one post/item
def deletePost(userID, PostID):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    q = """
    DELETE FROM posts
    WHERE UserID='"""+ str(userID) +"""'
    AND BlogID='"""+ str(PostID) +"""' 
    """
    c.execute(q)
    conn.commit()
    conn.close()
    
def deleteItem(userID, ItemID):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    q = """
    DELETE FROM posts
    WHERE UserID='"""+ str(userID) +"""'
    AND ItemID='"""+ str(ItemID) +"""' 
    """
    c.execute(q)
    conn.commit()
    conn.close()

def searchPost(title):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from posts where title = "'+title+'"')
    return c.fetchall()

    
#search items
#search posts
#edit items


