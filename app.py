import os
import env
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_pymongo import pymongo, PyMongo, DESCENDING
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import math
import re


app = Flask(__name__)
# SECRET KEY FOR CSRF #TODO + DB + MONGOURI
app.config['MONGO_DBNAME'] = 'book_review'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['SECRET_KEY'] = '8bf1555c499fe3cc55021fd1e87585e5'


mongo = PyMongo(app)


# ROUTE FOR LAYOUT
@app.route('/')
@app.route('/base')
def base():
    return render_template('base.html')


# ROUTE FOR INDEX.HTML
@app.route('/index', methods=['GET', 'POST'])
def index():
    # LANDING GETS 4 REVIEWS THAT HAVE THE MOST UPVOTES
    four_reviews = mongo.db.reviews.find().sort([('upvote', DESCENDING)]).limit(4)
    
    return render_template('index.html', title='Home', four_reviews=four_reviews)


#ROUTE FOR REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    #FUNCTION TO ALLOW A NEW USER TO REGISTER AND POST REVIEWS
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        #IF USER PASSES AUTHENTICATION
        user = mongo.db.users
        search_db = user.find_one({'username': request.form['username']})

        if search_db is None:
            #IF SEARCH RETURNS NO USERS
            pw_hash = generate_password_hash(request.form['password'])
            #ENCRYPTS PASSWORD
            user.insert_one({'username': request.form['username'],
                            'password': pw_hash,
                            'email': request.form['email']})
            #ALERT USER TO ACCOUNT CREATION
            flash('You now registered and logged in', 'success')
            session['username'] = request.form['username']
            session['logged_in'] = True
            return redirect(url_for('my_account'))
        else:
            #IF THAT DOESNT WORK
            flash('Oops, something happened. Try again.', 'warning')
            return redirect(url_for('register'))

    return render_template('register.html', title='Register', form=form)


#ROUTE FOR LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
        
    return render_template('login.html', title='Log In', form=form)


@app.route('/my_account')
def my_account():
    return render_template('my_account.html', title='My Account')

"""
@app.route('/add_review')
def add_review():
    user = mongo.db.reviews
    create_review = {'author': 'jack', 'title': 'My Toe', 'summary': 'how i stopped jamming'}
    add_review = mongo.db.reviews.insert_one(create_review)
    return 'review_added'
"""



if __name__ == '__main__':
            app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
