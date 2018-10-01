from poptraq import db
from datetime import datetime


class User(db.Model):
    """ Create user table"""

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    national_id = db.Column(db.Integer, nullable=False,)
    first_name = db.Column(db.String(80), nullable=False,)
    surname = db.Column(db.String(80), nullable=False,)
    dob = db.Column(db.Date, nullable=False,)
    home_county = db.Column(db.String(80), nullable=False,)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False,)
    created = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    last_seen = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)

    def __init__(self, national_id, first_name, surname, dob, home_county, email, password):
        self.national_id = national_id
        self.first_name = first_name
        self.surname = surname
        self.dob = dob
        self.home_county = home_county
        self.email = email
        self.password = password

    def __repr__(self):
        return '<user_id {}>'.format(self.user_id)


class County(db.Model):
    """County data"""

    __tablename__ = 'county'

    county_id = db.Column(db.Integer, nullable=False, primary_key=True)
    county_name = db.Column(db.String(80), nullable=False,)
    sub_county = db.Column(db.Integer, nullable=False,)
    sectors = db.Column(db.Integer, nullable=False,)
    population = db.Column(db.Float, nullable=False,)
    budget = db.Column(db.Float, nullable=False,)
    size = db.Column(db.Float, nullable=False,)

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
