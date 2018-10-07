from poptraq import db
from datetime import datetime
from flask_login import UserMixin
from poptraq import login


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """ Create user table"""

    __tablename__ = 'user'

    national_id = db.Column(db.Integer, nullable=False, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    home_county = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    last_seen = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String, nullable=False, default="User")

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
        return '<user_id {}>'.format(self.user_id)


class Admin(db.Model):
    """ Create user table"""

    __tablename__ = 'admin'

    national_id = db.Column(db.Integer, nullable=False, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    last_seen = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String, nullable=False, default="Admin")

    def __init__(self, national_id, first_name, surname, email, password):
        self.national_id = national_id
        self.first_name = first_name
        self.surname = surname
        self.email = email
        self.password = password

    def get_id(self):
        return self.national_id

    def __repr__(self):
        return '<admin_id {}>'.format(self.admin_id)


class County(db.Model):
    """County data"""

    __tablename__ = 'county'

    county_id = db.Column(db.Integer, nullable=False, primary_key=True)
    county_name = db.Column(db.String, nullable=False)
    sub_county = db.Column(db.Integer, nullable=False)
    sectors = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Float, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    # Allocated budget field, to add
    size = db.Column(db.Float, nullable=False)

    def __init__(self, county_id, county_name, sub_county, sectors, population, budget, size):
        self.county_id = county_id
        self.county_name = county_name
        self.sub_county = sub_county
        self.sectors = sectors
        self.population = population
        self.budget = budget
        self.size = size

    def __repr__(self):
        return '<county_id {}>'.format(self.county_id)
