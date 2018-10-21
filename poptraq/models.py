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

    county_code = db.Column(db.Integer, nullable=False, primary_key=True)
    county_name = db.Column(db.String, nullable=False)
    sub_county = db.Column(db.Integer, nullable=False)
    sectors = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Float, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    # Allocated budget field, to add
    size = db.Column(db.Float, nullable=False)

    def __init__(self, county_code, county_name, sub_county, sectors, population, budget, size):
        self.county_code = county_code
        self.county_name = county_name
        self.sub_county = sub_county
        self.sectors = sectors
        self.population = population
        self.budget = budget
        self.size = size

    def get_id(self):
        return self.county_code

    def __repr__(self):
        return '<county_id {}>'.format(self.county_id)
