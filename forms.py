from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length #validating data using wtf

class SignupForm(Form):
    first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")]) #validators make sure the field is not empty
    last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
    email = StringField('Email',validators=[DataRequired("Please enter your email."), Email("Please enter a valid email")])
    password = PasswordField('Password',validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more")])
    submit = SubmitField('Signup')

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired("Please enter your email."), Email("Please enter a valid email")])
    password = PasswordField('Password',validators=[DataRequired("Please enter a password.")])
    submit = SubmitField('Sign In')
