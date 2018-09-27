from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField, PasswordField
# importing necessary fields and validators for the form


class Signup(FlaskForm):
    """Template for signup form creation"""

    national_id = IntegerField("National ID", [validators.DataRequired(message="Kindly input your National ID Number")])
    first_name = StringField("First Name", [validators.DataRequired(message="Kindly your first name")])
    surname = StringField("Surname", [validators.DataRequired(message="Kindly input your last name")])
    dob = StringField("Date of Birth", [validators.DataRequired(message="Kindly input your Date of Birth")])
    email = StringField("Email", [validators.DataRequired(message="Kindly input your Email Address")])
    home_county = StringField("Home County", [validators.DataRequired(message="Kindly input your last name")])
    password = PasswordField("Password", [validators.DataRequired(message="Input Password"), validators.Length(min=8),
                                          validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = StringField("Repeat Password")


class Login(FlaskForm):
    """Template for Login Form creation"""

    national_id = IntegerField("National ID", [validators.DataRequired(message="National ID required")])
    email = StringField("Email", [validators.DataRequired(message="Email Address required")])
    password = PasswordField("Password", [validators.DataRequired(message="Password required")])
