import urllib2,json
from flask import Flask, render_template, redirect, url_for, request, Response

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def landing():
    if 'logged_in' not in session:
        session['logged_in'] = False
    if 'user' not in session:
        session['user'] = 'Anonymous'
    if request.method=="GET":
        if 'logged_in' not in session:
            return render_template("landing.html")
        
        else:        
            return render_template("home.html", user=session['user'])
            
    if request.method=="POST":
        button = request.form['button']
        username=request.form['username']
        password=request.form['password']
        if button=="Login":
            result = utils.authenticate(username,password)
            if result == "success":
                currentUser = username
                session['user'] = username
                session['logged_in'] = True
        
            elif result == "noUser":
            	return render_template("index.html", log = "noUser", s=session)
            else:
            	return render_template("index.html", log = "fail", s=session)
        else:
            return "bye"
            
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method=="GET":
    	return render_template("register.html", taken = False, success = False, s=session)
    if request.method=="POST":
        button = request.form['button']
        username=request.form['username']
        password=request.form['password']
        if button=="Register":
            response = utils.add(username,password)
            print response
            if response == "taken":
                return render_template("register.html", taken = True, success = False, s=session)
            elif response == "success":
                return render_template("register.html", taken = False, success = True, s=session)
            else:
                return "Wrong combo"
        else:
            return "bye"

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=8000)
