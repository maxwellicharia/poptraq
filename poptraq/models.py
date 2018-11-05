import pytz
from datetime import datetime

from flask_login import UserMixin

from poptraq import db
from poptraq import login_manager


@login_manager.user_loader
def load_user(login_id):
    return User.query.get(int(login_id))


class User(db.Model, UserMixin):
    """ Create user table"""

    d = datetime.now()
    timezone = pytz.timezone("Africa/Nairobi")
    d_aware = timezone.localize(d)

    __tablename__ = 'user'

    national_id = db.Column(db.Integer, nullable=False, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    home_county = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.String, nullable=False, default=d_aware.strftime("%B %d, %Y %H:%M:%S"))
    updated = db.Column(db.String, nullable=False, default=d_aware.strftime("%B %d, %Y %H:%M:%S"))
    last_seen = db.Column(db.String, nullable=False, default=d_aware.strftime("%B %d, %Y %H:%M:%S"))
    confirmed = db.Column(db.Boolean, nullable=True)
    confirmed_on = db.Column(db.String, nullable=True)
    user = db.Column(db.Boolean, nullable=False, default=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String, nullable=False, default='Active')

    def __init__(self, national_id, first_name, surname, dob, home_county, email, password):
        self.national_id = national_id
        self.first_name = first_name
        self.surname = surname
        self.dob = dob
        self.home_county = home_county
        self.email = email
        self.password = password

    def get_id(self):
        return self.national_id

    def __repr__(self):
        return '<national_id {}>'.format(self.national_id)


class County(db.Model):
    """County data"""

    __tablename__ = 'county'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    county_name = db.Column(db.String, nullable=False, unique=True)
    sectors = db.Column(db.Integer, nullable=True)
    population = db.Column(db.Integer, nullable=True)
    current_budget = db.Column(db.Float, nullable=True)
    proposed_budget = db.Column(db.Float, nullable=True)
    size = db.Column(db.Float, nullable=False)

    def __init__(self, county_name, size):
        self.county_name = county_name
        self.size = size

    def __repr__(self):
        return '<county_id {}>'.format(self.county_id)


class Details(db.Model):
    """User Details"""

    __tablename__ = 'details'
    national_id = db.Column(db.Integer, nullable=False, primary_key=True)
    photo = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    specifics = db.Column(db.Text, nullable=False)

    def __init__(self, photo, age, gender, status, specifics):
        self.photo = photo
        self.age = age
        self.gender = gender
        self.status = status
        self.specifics = specifics
