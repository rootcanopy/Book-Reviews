import os
import env
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_pymongo import pymongo, PyMongo, DESCENDING
from bson.objectid import ObjectId
#from forms import RegistrationForm, LoginForm, ReviewForm
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
    return render_template('register.html', title='Register')


#ROUTE FOR LOGIN
@app.route('/')
def login():
    return render_template('login', title='Log In')





@app.route('/add_review')
def add_review():
    user = mongo.db.reviews
    create_review = {'author': 'jack', 'title': 'My Toe', 'summary': 'how i stopped jamming'}
    add_review = mongo.db.reviews.insert_one(create_review)
    return 'review_added'




if __name__ == '__main__':
            app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
