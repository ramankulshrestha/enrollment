from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import sqlite3
#from application.models import User
class LoginForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
   # remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login Now")

class RegisterForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')])
    name =StringField("Name", validators=[DataRequired(),Length(min=2,max=55)])
    address = StringField("Address", validators=[DataRequired(),Length(min=10,max=200)])
    amount = StringField("Amount to be paid", validators=[DataRequired(),Length(min=2,max=10)])
    submit = SubmitField("Register Now")

class PayForm(FlaskForm):
    memberid  = StringField("Member Id")
    memberName  = StringField("Member Name")
    memberAddress  = StringField("Address")
    paydate = StringField("Payment Date", validators=[DataRequired()])
    payAmount = StringField("Payment Amount", validators=[DataRequired()])
    payReference = StringField("Payment Reference", validators=[DataRequired()])
    submit = SubmitField("Pay Now")



 
