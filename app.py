import urllib2,json
from flask import Flask, render_template, redirect, url_for, request, Response, session
import utils

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def landing():
    if request.method== "GET":
        if 'logged_in' not in session:
            session['logged_in'] = False
        if 'logged_in':
            return render_template("landing.html")
        else:        
            return render_template("home.html", user=session['user'])
    if request.method == "POST":
        button = request.form['button']
        #Login procedure
        if button == "Login":
            username=request.form['username']
            password=request.form['password']
            result = utils.authenticate(username,password)
            if result:
                currentUser = username
                session['user'] = username
                session['logged_in'] = True
                return render_template("home.html",user=username)
            else:
            	return render_template("landing.html", loginerror = "Username and password do not match!")
        #Register procedure
        if button == "Register":
            username=request.form['r_username']
            password1=request.form['r_password1']
            password2=request.form['r_password2']
            #password match check
            if (password1 == password2):
                #username and password lengths check
                if len(username)<4:
                    return render_template('landing.html',registererror="Username must be longer than 4 characters")
                if len(password1)<4:
                    return render_template('landing.html',registererror="Password must be longer than 4 characters")
                if utils.newUser(username,password1):
                    return render_template("home.html");
                else:
                    return render_template("landing.html",registererror="Username already taken");
            else:
                return render_template("landing.html",registererror="Passwords do not match!");
        else:
            render_template("landing.html");

if __name__ == "__main__":
    app.debug = True    
    app.secret_key="stuylegacy"
    app.run(host="0.0.0.0",port=8000)
