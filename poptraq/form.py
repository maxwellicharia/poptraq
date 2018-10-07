from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, IntegerField, PasswordField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from poptraq.models import User


class RegistrationForm(FlaskForm):
    """Template for signup form creation"""

    national_id = IntegerField("National ID", [DataRequired(message="Kindly input your National ID Number")])
    first_name = StringField("First Name", [DataRequired(message="Kindly your first name")])
    surname = StringField("Surname", [DataRequired(message="Kindly input your last name")])
    dob = StringField("Date of Birth", [DataRequired(message="Kindly input your Date of Birth")])
    email = StringField("Email", [DataRequired(message="Kindly input your Email Address"), Email(
        message="Invalid Email Address, missing '@' symbol")])
    home_county = StringField("Home County", [DataRequired(message="Kindly input your last name")])
    password = PasswordField("Password", [DataRequired(message="Input Password"),
                                          Length(min=8, message="Password too short > 8"), Length(max=16),
                                          EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Repeat Password", [DataRequired(message="Confirm Password"),
                                                         EqualTo('password', message='Passwords must match')])
    recaptcha = RecaptchaField()
    remember_me = BooleanField('Remember Me')

    def validate_national_id(self, national_id):
        user = User.query.filter_by(national_id=national_id.data).first()
        if user is not None:
            raise ValidationError('National ID already used by a different user.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address already exists')


class LoginForm(FlaskForm):
    """Template for Login Form creation"""

    national_id = IntegerField("National ID", [DataRequired(message="National ID required")])
    email = StringField("Email", [DataRequired(message="Email Address required"), Email(
        message="Invalid Email Address, missing '@' symbol")])
    password = PasswordField("Password", [DataRequired(message="Password required")])
    recaptcha = RecaptchaField()
    remember_me = BooleanField('Remember Me')


class County(FlaskForm):
    """County Template for data display"""

    county_name = StringField("County Name", [DataRequired(message="Name of county required")])
    sub_counties = IntegerField("No. of Sub-counties", [DataRequired(message="Required field")])
    sectors = IntegerField("No. of sectors", [DataRequired(message="Input County Government Sectors")])
    population = FloatField("Population", [DataRequired(message="Input estimated calculated population")])
    budget = FloatField("Budget (Ksh)", [DataRequired(message="Input allocated budget")])
    size = FloatField("County Size", [DataRequired(message="Input county size")])


class EmailForm(FlaskForm):
    national_id = IntegerField("National ID", [DataRequired(message="National ID required")])
    email = StringField("Email", [DataRequired(message="Email Address required"), Email(
        message="Invalid Email Address, missing '@' symbol")])
    recaptcha = RecaptchaField()


class PasswordForm(FlaskForm):
    national_id = IntegerField("National ID", [DataRequired(message="National ID required")])
    email = StringField("Email", [DataRequired(message="Email Address required"), Email(
        message="Invalid Email Address, missing '@' symbol")])
    password = PasswordField("Password", [DataRequired(message="Input Password"),
                                          Length(min=8, message="Password too short > 8"),
                                          EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Repeat Password", [DataRequired(message="Confirm Password"),
                                                         EqualTo('password', message='Passwords must match')])
    recaptcha = RecaptchaField()
