import urllib2,json
from flask import Flask, render_template, redirect, url_for, request, Response, session

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def landing():
    if 'logged_in' not in session:
        session['logged_in'] = False
    if 'user' not in session:
        session['user'] = 'Anonymous'
    if request.method=="GET":
        if 'logged_in':
            return render_template("landing.html")
        
        else:        
            return render_template("home.html", user=session['user'])

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("landing.html")
    if request.method=="POST":
        button = request.form['button']
        username=request.form['username']
        password=request.form['password']
        print button
        print username
        print password
        if button=="Login":
            result = utils.authenticate(username,password)
            if result == "success":
                currentUser = username
                session['user'] = username
                session['logged_in'] = True
                return render_template("home.html",user=username)
            else:
            	return render_template("landing.html", loginerror = "Username and password do not match!")
        else:
            return "bye"
            
@app.route("/register", methods = ["POST"])
def register():
    if request.method=="POST":
        r_username=request.form['r_username']
        r_password=request.form['r_password']
        r_password2=request.form['r_password2']
        if button=="Register":
            if r_password == r_password2:
                response = utils.add(r_username,r_password)
                print response
                if response == "taken":
                    return render_template("register.html", taken = True, success = False, s=session)
                elif response == "success":
                    return render_template("register.html", taken = False, success = True, s=session)
                else:
                    return "Wrong combo"
            else:
                print "Passwords don't match"
        else:
            return "bye"
        
if __name__ == "__main__":
    app.debug = True    
    app.secret_key="stuylegacy"
    app.run(host="0.0.0.0",port=8000)
