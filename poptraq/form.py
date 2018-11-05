from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, IntegerField, PasswordField, FloatField, BooleanField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES
from datetime import datetime
from datetime import date

from poptraq.models import User

images = UploadSet('images', IMAGES)


def calculate_age(dt):
    birth = datetime.strptime(dt, '%Y-%m-%d')
    today = date.today()
    print(float(today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))), )
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


class RegistrationForm(FlaskForm):
    """Template for signup form creation"""

    national_id = IntegerField("National ID", [DataRequired(message="Kindly input your National ID Number")])
    first_name = StringField("First Name", [DataRequired(message="Kindly your first name")])
    surname = StringField("Surname", [DataRequired(message="Kindly input your last name")])
    dob = DateField('Date of Birth', [DataRequired(message="Kindly input your Date of Birth")])
    email = EmailField("Email", [DataRequired(message="Kindly input your Email Address"),
                                 Email(message="Invalid Email Address, missing '@' symbol")])
    home_county = SelectField('County', [DataRequired(message="Kindly select home county")],
                              choices=[('Mombasa', 'Mombasa'), ('Kwale', 'Kwale'), ('Kilifi', 'Kilifi'),
                                       ('Tana River', 'Tana River'), ('Lamu', 'Lamu'), ('Taita-Taveta', 'Taita-Taveta'),
                                       ('Garissa', 'Garissa'), ('Wajir', 'Wajir'), ('Mandera', 'Mandera'),
                                       ('Marsabit', 'Marsabit'), ('Isiolo', 'Isiolo'), ('Meru', 'Meru'),
                                       ('Tharaka-Nithi', 'Tharaka-Nithi'), ('Embu', 'Embu'), ('Kitui', 'Kitui'),
                                       ('Machakos', 'Machakos'), ('Makueni', 'Makueni'), ('Nyandarua', 'Nyandarua'),
                                       ('Nyeri', 'Nyeri'), ('Kirinyaga', 'Kirinyaga'), ('Murang\'a', 'Murang\'a'),
                                       ('Kiambu', 'Kiambu'), ('Turkana', 'Turkana'), ('West Pokot', 'West Pokot'),
                                       ('Samburu', 'Samburu'), ('Trans-Nzoia', 'Trans-Nzoia'),
                                       ('Uasin Gishu', 'Uasin Gishu'), ('Elgeyo-Marakwet', 'Elgeyo-Marakwet'),
                                       ('Nandi', 'Nandi'), ('Baringo', 'Baringo'), ('Laikipia', 'Laikipia'),
                                       ('Nakuru', 'Nakuru'), ('Narok', 'Narok'), ('Kajiado', 'Kajiado'),
                                       ('Kericho', 'Kericho'), ('Bomet', 'Bomet'), ('Kakamega', 'Kakamega'),
                                       ('Vihiga', 'Vihiga'), ('Bungoma', 'Bungoma'), ('Busia', 'Busia'),
                                       ('Siaya', 'Siaya'), ('Kisumu', 'Kisumu'), ('Homa Bay', 'Homa Bay'),
                                       ('Migori', 'Migori'), ('Kisii', 'Kisii'), ('Nyamira', 'Nyamira'),
                                       ('Nairobi', 'Nairobi')])
    password = PasswordField("Password", [DataRequired(message="Input Password"),
                                          Length(min=8, message="Password too short > 8"),
                                          Length(max=16),
                                          EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Repeat Password", [DataRequired(message="Confirm Password"),
                                                         EqualTo('password', message='Passwords must match')])
    recaptcha = RecaptchaField()
    remember_me = BooleanField('Remember Me')

    def validate_national_id(self, national_id):
        form = RegistrationForm()
        user = User.query.filter_by(national_id=national_id.data).first()
        if user is not None:
            raise ValidationError('National ID already used by a different user')
        if not int(form.national_id.data):
            raise ValidationError('Only numbers allowed on this input')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address already exists')

    def validate_first_name(self, first_name):
        if not str(first_name):
            raise ValidationError('No special characters eg.(@, #, [space]) allowed, only letters')

    def validate_surname(self, surname):
        if not str(surname):
            raise ValidationError('No special characters eg.(@, #, [space]) allowed, only letters')

    def validate_dob(self, dob):
        form = RegistrationForm()
        if calculate_age(str(form.dob.data)) < 18:
            raise ValidationError('Invalid date of birth, age is less than 18 years')
        if calculate_age(str(form.dob.data)) > 120:
            raise ValidationError('Invalid date of birth, age more than 120 years')


class LoginForm(FlaskForm):
    """Template for Login Form creation"""

    national_id = IntegerField("National ID", [DataRequired(message="National ID required")])
    email = EmailField("Email", [DataRequired(message="Email Address required"),
                                 Email(message="Invalid Email Address, missing '@' symbol")])
    password = PasswordField("Password", [DataRequired(message="Password required")])
    recaptcha = RecaptchaField()
    remember_me = BooleanField('Remember Me')


class AdminForm(FlaskForm):
    pass


class CountyForm(FlaskForm):
    """County Template for data display"""

    county_name = SelectField('County', [DataRequired(message="Kindly select home county")],
                              choices=[('Mombasa', 'Mombasa'), ('Kwale', 'Kwale'), ('Kilifi', 'Kilifi'),
                                       ('Tana River', 'Tana River'), ('Lamu', 'Lamu'), ('Taita-Taveta', 'Taita-Taveta'),
                                       ('Garissa', 'Garissa'), ('Wajir', 'Wajir'), ('Mandera', 'Mandera'),
                                       ('Marsabit', 'Marsabit'), ('Isiolo', 'Isiolo'), ('Meru', 'Meru'),
                                       ('Tharaka-Nithi', 'Tharaka-Nithi'), ('Embu', 'Embu'), ('Kitui', 'Kitui'),
                                       ('Machakos', 'Machakos'), ('Makueni', 'Makueni'), ('Nyandarua', 'Nyandarua'),
                                       ('Nyeri', 'Nyeri'), ('Kirinyaga', 'Kirinyaga'), ('Murang\'a', 'Murang\'a'),
                                       ('Kiambu', 'Kiambu'), ('Turkana', 'Turkana'), ('West Pokot', 'West Pokot'),
                                       ('Samburu', 'Samburu'), ('Trans-Nzoia', 'Trans-Nzoia'),
                                       ('Uasin Gishu', 'Uasin Gishu'), ('Elgeyo-Marakwet', 'Elgeyo-Marakwet'),
                                       ('Nandi', 'Nandi'), ('Baringo', 'Baringo'), ('Laikipia', 'Laikipia'),
                                       ('Nakuru', 'Nakuru'), ('Narok', 'Narok'), ('Kajiado', 'Kajiado'),
                                       ('Kericho', 'Kericho'), ('Bomet', 'Bomet'), ('Kakamega', 'Kakamega'),
                                       ('Vihiga', 'Vihiga'), ('Bungoma', 'Bungoma'), ('Busia', 'Busia'),
                                       ('Siaya', 'Siaya'), ('Kisumu', 'Kisumu'), ('Homa Bay', 'Homa Bay'),
                                       ('Migori', 'Migori'), ('Kisii', 'Kisii'), ('Nyamira', 'Nyamira'),
                                       ('Nairobi', 'Nairobi')])
    size = FloatField("County Size", [DataRequired(message="Input county size")])


class EmailForm(FlaskForm):
    email = EmailField("Email", [DataRequired(message="Email Address required"), Email(
        message="Invalid Email Address, missing '@' symbol")])
    recaptcha = RecaptchaField()


class PasswordForm(FlaskForm):
    password = PasswordField("Password", [DataRequired(message="Input Password"),
                                          Length(min=8, message="Password too short > 8"),
                                          EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Repeat Password", [DataRequired(message="Confirm Password"),
                                                         EqualTo('password', message='Passwords must match')])
    recaptcha = RecaptchaField()


class SearchForm(FlaskForm):
    email = EmailField()


class DetailsForm(FlaskForm):
    passport_photo = FileField("Passport Photo", validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')])
    age = IntegerField()
    gender = SelectField('Gender', [DataRequired(message="Kindly select your gender")],
                         choices=[('Female', 'Female'), ('Male', 'Male')])
    marital_status = SelectField('Marital Status', [DataRequired(message="Kindly select your status")],
                                 choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'),
                                          ('Separated', 'Separated')])
    specifics = TextAreaField('Specify your status, N/A if individual',
                              [DataRequired(message="Update details regarding your status")])
