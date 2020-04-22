from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,\
                    SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, \
                            EqualTo, Email
from flask_wtf.file import FileField, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password_repeat', message='Passwords must match')])                                   
    password_repeat = PasswordField('Repeat Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')

class ReviewForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired()])          
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('Summary',validators=[DataRequired()])
    review = TextAreaField('Review',validators=[DataRequired()])
    image = FileField('Image Only')
    ratings = IntegerField('Rating', validators=[DataRequired()])
    add_review = SubmitField('Add Review')