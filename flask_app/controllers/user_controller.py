from flask_app import app
from flask import render_template, session,flash,redirect,request
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/adduser",methods=["post"])
def adduser():
    if User.validate_new(request.form):
        pw_hash=bcrypt.generate_password_hash(request.form["password"])
        data={
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "password":pw_hash,
            "confirm":request.form["confirm"],
        }
        User.add_new(data)
        return redirect("/dashboard")
    return redirect("/")

@app.route('/login', methods=['POST'])
def login():
    if  User.validate_login(request.form):
        logged_user=User.get_by_email(request.form)
        session['user_id'] = logged_user.id
        return redirect("/dashboard")
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please Login")
        return redirect("/")

    data={
        "user_id":session["user_id"]
    }
    user=User.get_by_id(data)

    return render_template("dashboard.html",user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
