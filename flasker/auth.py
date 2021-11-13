from flask import Blueprint,render_template,request,flash, g, redirect,session, url_for
from .models import User,db
from flasker import home
import functools
from flasker import login_required
auth = Blueprint('auth',__name__)



#---------------------LOGIN--------------------------

@auth.route("/login",methods=["GET","POST"])
def user_login():
    if "user_id" in session:
        return redirect(url_for("home.index"))
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        error = None
        user = User.query.filter_by(email=email).first()
        
        if user is None:
            return "User Not Exist"
        if user.password != password:
            return "password dose not match"
        if user and password:
            session.clear()
            session["user_id"] = user.id
            loggin = True
            return redirect(url_for("home.index"))
    return render_template("login.html")

@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()

@login_required
@auth.route("/logout")
def user_logout():
    session.clear()
    return redirect(url_for("auth.user_login"))

@auth.route("/register",methods=["GET","POST"])
def user_register():
    if "user_id" in session:
        return redirect(url_for("home.index"))
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        print(username,email,password)
        user = User(username=username,email=email,password=password)
        db.session.add(user)
        db.session.commit()
    return render_template("singup.html")


