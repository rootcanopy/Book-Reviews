import os
import env
from flask import Flask, render_template, redirect, \
        url_for, flash, request, session
from flask_pymongo import pymongo, PyMongo, DESCENDING
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm, ReviewForm
from werkzeug.security import generate_password_hash, check_password_hash
import math
import re


app = Flask(__name__)
# SECRET KEY FOR CSRF + DB + MONGOURI
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['MONGO_DBNAME'] = 'book_review'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


# ROUTE FOR INDEX.HTML
@app.route('/')
@app.route('/index')
def index():
    # LANDING GETS 4 REVIEWS THAT HAVE THE MOST UPVOTES
    four_reviews = mongo.db.reviews.find().sort([('upvote', DESCENDING)]).limit(4)
    return render_template('index.html',  title='Home', reviews=four_reviews)


# ROUTE FOR REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    # FUNCTION TO ALLOW A NEW USER TO REGISTER AND POST REVIEWS
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        # IF USER PASSES AUTHENTICATION
        user = mongo.db.users
        search_db = user.find_one({'username': request.form['username']})
        # USER ISINT REGISTERED
        if search_db is None:
            # IF SEARCH RETURNS NO USERS
            pw_hash = generate_password_hash(request.form['password'])
            # ENCRYPTS PASSWORD
            user.insert_one({'username': request.form['username'],
                            'password': pw_hash,
                            'email': request.form['email']})
            # ALERT USER TO ACCOUNT CREATION
            flash('You now registered and logged in', 'success')
            session['username'] = request.form['username']
            session['logged_in'] = True
            return redirect(url_for('my_account'))
        else:
            # IF THAT DOESNT WORK
            flash('Oops, something happened. Try again.', 'warning')
            return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


# ROUTE FOR LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    # THE USER LOGIN FUNCTION
    form = LoginForm()
    # LOGIN HANDLER
    if session.get('logged_in'):
        if session['logged_in'] is True:
            return redirect(url_for('home'))
    if form.validate_on_submit():
        # IF LOG IN FORM PASSES VALIDATION
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user:  # IF USER IN DB
            password = form.password.data
            if check_password_hash(existing_user['password'], password):
                # IF THE HASH FITS
                session['username'] = request.form['username']
                session['logged_in'] = True
                # IF SUCCESS REDIRECT TO HOME
                return redirect(url_for('index', title='Home', form=form))
            # IF FAILS
            flash('Invalid username/password combination')
    return render_template('login.html', title='Log In', form=form)


# ROUTE TO ACCOUNT
@app.route('/my_account/')
def my_account():
    # FOR USER ACCOUNT
    if 'logged_in' in session:
        # ASSIGNING CU ATTRIB
        current_user = session['username']
        # MESSAGE TO GREET USER
        flash('Hi "' + current_user + '". This is your profile, add \
                or edit your reviews', 'success')
        # GETTING USER DETAILS FOR ACCOUNT
        search_user = mongo.db.users.find_one({'username': current_user})
        # USERS REVIEW HISTORY
        reviews = mongo.db.reviews.find_one({'username': current_user})
        loop = mongo.db.reviews.count_documents({'username': current_user})  # TODO
    return render_template('my_account.html', title='My Account',
                            loop=loop, users=search_user,
                            reviews=reviews)


# TO REMOVE/DELETE ACCOUNT
@app.route('/delete_account/<id>', methods=['GET', 'POST'])
def delete_account(id):
    # DETAILS FROM LOGGED IN
    users = session['username']
    # REMOVING ALL BY USER
    mongo.db.reviews.delete_many({'username': users})
    # REMOVING ACCOUNT
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    # SESSION POPPED
    session.clear()

    flash('Your account has been removed', 'success')
    return redirect(url_for('index'))


# ROUTE FORM ADD REVIEW
@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    form = ReviewForm()
    if form.validate_on_submit():
        reviews = mongo.db.reviews
        # ADD A RECORD
        reviews.insert_one({
            'author': request.form['author'],
            'title': request.form['title'],
            'summary': request.form['summary'],
            'review': request.form['review'],
            'username': session['username']
        })
        flash('You have a reviewed a book', 'success')
        # SENDS TO REVIEWS UPON SUCCESS
        return redirect(url_for('my_reviews'))
    return render_template('add_review.html', title='Add Review', form=form)


# FUNCTION TO EDIT REVIEW
@app.route('/edit_review/<id>', methods=['GET', 'POST'])
def edit_review(id):
    one_rev = mongo.db.reviews.find_one({'_id': ObjectId(id)})
    form = ReviewForm(data=one_rev)
    if form.validate_on_submit():
        reviews = mongo.db.reviews
        # THE DOCUMENT MODEL
        reviews.update_one({'_id': ObjectId(id)}, {'$set': {
            'author': request.form['author'],
            'title': request.form['title'],
            'summary': request.form['summary'],
            'review': request.form['review'],
            'image': request.form['image_file'],
            'vote': 0
            }})
        flash('Updated', 'success')
    return render_template('edit_review.html', form=form,
                            title='Edit Review')

# ROUTE FOR REVIEW PAGE
@app.route('/reviews/<id>', methods=['GET', 'POST'])
def reviews(id):
    # FUNCTION DISPLAYS DOC OF REVIEW IF ID
    # RUNS WHEN CLICKED
    one_rev = mongo.db.reviews.find_one({'_id': ObjectId(id)})
    title = one_rev['title']
    format_rev = one_rev['review']
    # PASS LIST INTO TEMPLATE FOR LOOP
    format_rev = re.split(r"[~\r\n]+", format_rev)
    return render_template('reviews.html', review=one_rev,
                            title=title, format_rev=format_rev)


# DELETE A RREVIEW
@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete_review(id):
    # LETS LOGGED IN DELETE THEIR REVIEW
    # GETS THE REVIEW
    one_rev = mongo.db.reviews.find_one({'_id': ObjectId(id)})
    if one_rev['username'] == session['username']:
        flash('You have deleted your review', 'success')
    mongo.db.reviews.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))


# THE LOGGED IN USERS REVIEWS
@app.route('/my_reviews', methods=['GET', 'POST'])
def my_reviews():
    if 'logged_in' in session:
        flash('This is your reviews page', 'success')
        # UPON ARRIVING ON USER REVIEW PAGE
        current_user = session['username']
        # SEARCH DB FOR USERS REVIEWS
        reviews = mongo.db.reviews.find({'username': current_user})
    return render_template('my_reviews.html', title='My Reviews',
                            reviews=reviews)


# USER SIGN OUT
@app.route('/logout')
def logout():
    # SIGNS USER OUT AND CLEARS SESSION
    session.clear()
    flash('You have logged out', 'success')
    return render_template('index.html', title='Home')


# APP RUN
if __name__ == '__main__':
        app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
