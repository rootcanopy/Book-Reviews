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
    #THE USER LOGIN FUNCTION
    form = LoginForm()
    # LOGIN HANDLER
    if session.get('logged_in'):
        if session['logged_in'] is True:
            return redirect(url_for('home'))

    if form.validate_on_submit():

        # if log in form passes all validation check if username  exists
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})
        
        if existing_user:  #IF USER IN DB
            password = form.password.data
            if check_password_hash(existing_user['password'], password):
                # IF THE HASH FITS
                session['username'] = request.form['username']
                session['logged_in'] = True
                #IF SUCCESS REDIRECT TO HOME
                return redirect(url_for('home', title='Log In', form=form))
            #IF FAILS
            flash('Invalid username/password combination')
    return render_template('login.html', title='Log In', form=form)


@app.route('/my_account/')
def my_account():
    #FOR USER ACCOUNT
    if 'logged_in' in session:
        current_user = session['username']
        flash('Hi "' + current_user + '". This is your profile, add or edit your reviews', 'success')

        search_user = mongo.db.users.find_one({'username': current_user})

        reviews = mongo.db.reviews.find({'username': current_user})
        loop = mongo.db.reviews.count_documents({'username': current_user})
    return render_template('my_account.html', title='My Account',reviews=reviews, loop=loop, users=search_user)

"""
@app.route('/add_review')
def add_review():
    user = mongo.db.reviews
    create_review = {'author': 'jack', 'title': 'My Toe', 'summary': 'how i stopped jamming'}
    add_review = mongo.db.reviews.insert_one(create_review)
    return 'review_added'
"""

#TO REMOVE/DELETE ACCOUNT
@app.route('/delete_account/<id>', methods=['GET', 'POST'])
def delete_account(id):
    users = session['username']
    mongo.db.reviews.delete_many({'username': users})
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    session.clear()

    flash('Your account has been deleted', 'success')
    return redirect(url_for('index',))


if __name__ == '__main__':
            app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
