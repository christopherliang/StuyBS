import urllib2,json
from flask import Flask, render_template, redirect, url_for, request, Response, session
import utils

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
@app.route("/home/", methods=["GET","POST"])
def home():
    if request.method== "GET":
        return render_template("home.html")
    if request.method == "POST":
        button = request.form['button']
        #Login procedure
        if button == "Login":
            username=request.form['username']
            password=request.form['password']
            if utils.authenticate(username,password):
                if 'n' not in session:
                    session['n'] = username
                    return render_template("home.html")
            else:
                return render_template("home.html",loginerror="Invalid Username or Password")
        #Register procedure
        if button == "Register":
            username=request.form['r_username']
            password1=request.form['r_password1']
            password2=request.form['r_password2']
            #password match check
            if (password1 == password2):
                #username and password lengths check
                if len(username)<4:
                    return render_template('home.html',registererror="Username must be longer than 4 characters")
                if len(password1)<4:
                    return render_template('home.html',registererror="Password must be longer than 4 characters")
                if utils.newUser(username,password1):
                    return render_template("home.html",registererror="Account created successfully")
                else:
                    return render_template("home.html",registererror="Username already taken")
            else:
                return render_template("home.html",registererror="Passwords do not match!")
        else:
            return render_template("home.html")

@app.route('/logout', methods=['GET','POST'])
def logout():
    #remove the username from the session if it's there
    session.pop('n', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.debug = True    
    app.secret_key="stuylegacy"
    app.run(host="0.0.0.0",port=8000)
