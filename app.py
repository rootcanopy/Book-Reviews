import os
import env
import math
import re
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm, ReviewForm
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)


# SECRET KEY FOR CSRF #TODO + DB + MONGOURI
app.config['MONGO_DBNAME'] = 'book_review'
app.config['SECRET_KEY'] = '8bf1555c499fe3cc55021fd1e87585e5'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


# ROUTE FOR INDEX.HTML