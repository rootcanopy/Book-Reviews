import os
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_pymongo import PyMongo, DESCENDING
from bson.objectid import ObjectId
#from forms import RegistrationForm, LoginForm, ReviewForm
from werkzeug.security import generate_password_hash, check_password_hash
import env
import math
import re

app = Flask(__name__)


# SECRET KEY FOR CSRF #TODO + DB + MONGOURI
app.config['MONGO_DBNAME'] = 'book_review'
app.config['SECRET_KEY'] = '8bf1555c499fe3cc55021fd1e87585e5'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


# ROUTE FOR INDEX.HTML
@app.route('/')
@app.route('/index')
def index():
    # LANDING GETS 4 REVIEWS THAT HAVE THE MOST UPVOTES
    four_books = mongo.db.reviews.find().sort([('upvotes', DESCENDING)]).limit(4)
    return render_template('index.html', title='Home', reviews=four_books)







if __name__ == '__main__':
            app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
