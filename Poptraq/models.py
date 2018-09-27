from app import db


class User(db.Model):
    """ Create user table"""
    national_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    dob = db.Column(db.String(25))
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
