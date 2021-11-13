from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, PasswordField, SelectField, RadioField, IntegerField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from app.models import *

from flask import flash


class LoginForm(Form):
	user_name = StringField('user_name', validators=[DataRequired()])
	password = PasswordField('password',validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)
	submit = SubmitField('Sign In')
	
	

















								