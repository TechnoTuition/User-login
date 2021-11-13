from flask import Blueprint,render_template,session,redirect,url_for
from .auth import user_login
from flasker import login_required
from .models import User
import functools

home = Blueprint('home',__name__)




@login_required
@home.route("/")
def index():
    if "user_id" in session:
        id = session["user_id"]
        user = User.query.filter_by(id=id).first() 
        loggin = True
        return render_template("index.html",u=user)
    
    elif "user_id" != session:
        return redirect(url_for("auth.user_login"))
    return render_template("index.html")