import sqlite3
import md5;
import re;

#sanitizes username 
def sanitize(input):
    return re.sub('"', "  ", input)

#hashes password
def encrypt(username,password):
    m = md5.new()
    m.update(username+password)
    return m.hexdigest()
    #hashes and salts the pasword for permanent storage or retrieval
    #returns hashed password

#checks if username and password match
def authenticate(username, password):
    username = sanitize(username)
    conn = sqlite3.connect("bs.db")
    c = conn.cursor()
    ans = c.execute('select * from users where username = "'+username+'" and password = "'+encrypt(username,password)+'";') 
    for r in ans:
        return True;
    return False;
    #returns a boolean that describes whether the user has succesfully logged in.

#counts number of users and assigns next ID for a new user
def countUserID():
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from users;')
    items = c.fetchall()
    n = 0
    for i in items:
        n = n + 1
    return n

#gets the id of a user as an int
#username is text
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

#creates a new user
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

#changes password
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

#gets all items
#returns array of all items
def getAllItems():
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from items;')
    return c.fetchall()

#gets all posts
#returns array of all posts
def getAllPosts():
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from posts;')
    return c.fetchall()

#add item
#name, category, description are string
#price and condition are ints
#user is used to find userID
def addItem(name, price, condition, category, description,user):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('insert into items values("'+name+'","'+str(price)+'","'+str(condition)+'","'+category+'","'+description+'","'+str(getItemID() + 1)+'","'+str(getUserID(user))+'")')
    conn.commit()

#add post
#tite and content are string
#user is used to find ID
def addPost(title,content,user):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('insert into posts values("'+content+'","'+title+'","'+str(getPostID() + 1)+'","'+str(getUserID(user))+'")')
    conn.commit()

#counts number of items
#used to assign new items an ID
def getItemID():
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from items;')
    items = c.fetchall()
    n = 0
    for i in items:
        n = n + 1
    return n

#counts number of posts
#used to assign new posts an ID
def getPostID():
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from posts;')
    posts = c.fetchall()
    n = 0
    for p in posts:
        n = n + 1
    return n

#edits the posts contents
#userID and postID are ints used to find the specific post
#new_content is a string
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

#userID and postID are ints
#to find specific post
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

#delete a users item up for sale
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

#searches posts
#returns array of all posts with title
#title is a string
def searchPost(title):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from posts where title = "'+title+'"')
    return c.fetchall()

#searches item name
#returns array of all items
#query is a string
def searchItem(query):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from items where name = "'+query+'" or category = "'+query+'" or instr(description, "'+query+'") != 0')        
    return c.fetchall()

#find items less than price
#returns array of all items with with a price less than price
#price is an int
def filterByPrice(price):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from items where price <= "'+str(price)+'"')
    return c.fetchall()

#find items in category
#returns array of all items in that category
#category is a string
def filterByCategory(category):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('select * from items where category = "'+category+'"')
    return c.fetchall()

#add comments to posts
#content is a string
#blogID is an int to find the specific post
#user to get a userID
def Comment(content,blogID,user):
    conn = sqlite3.connect('bs.db')
    c = conn.cursor()
    c.execute('insert into comments values("'+content+'","'+str(blogID)+'","'+str(getUserID(user))+'")')
    conn.commit()

