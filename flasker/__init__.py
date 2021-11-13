from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
import functools
from datetime import timedelta


app = Flask(__name__)
#----------------session-------+--+------------

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1440)
    
#----------------- login required---------------------
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.index'))

        return view(**kwargs)

    return wrapped_view



#------------------SECRETS_KEY-------------------------
app.config['SECRET_KEY'] = 'a72c3251c8451aed32520c20b1ab7475'

#--------------------DATABASE--------------------------

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#--------------------App Register---------------------
from .home import home
from .auth import auth

app.register_blueprint(auth,url_prefix='/auth')
app.register_blueprint(home,url_prefix='/')