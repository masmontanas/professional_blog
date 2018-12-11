from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask import request

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EmailSubscribeForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    subscribe = SubmitField('Subscribe')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contactemail = StringField('Email', validators=[DataRequired(), Email()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    comment = StringField('Comment', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    q = StringField(('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)