from poptraq import db


class User(db.Model):
    """ Create user table"""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    national_id = db.Column(db.Integer)
    first_name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    dob = db.Column(db.Date)
    home_county = db.Column(db.String(80))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, national_id, first_name, surname, dob, home_county, email, password):
        self.national_id = national_id
        self.first_name = first_name
        self.surname = surname
        self.dob = dob
        self.home_county = home_county
        self.email = email
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)


class County(db.Model):
    """County data"""

    __tablename__ = 'county'

    id = db.Column(db.Integer, primary_key=True)
    county_name = db.column(db.String(80))
    sub_county = db.Column(db.Integer)
    sectors = db.Column(db.Integer)
    population = db.Column(db.Float)
    budget = db.Column(db.Float)
    size = db.Column(db.Float)

    def __repr__(self):
        return '<id {}>'.format(self.id)
