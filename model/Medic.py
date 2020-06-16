from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from utils.extensions import db


class Medic(UserMixin, db.Model):
    __tablename__ = 'medici'
    id = db.Column(db.Integer(), primary_key=True)
    nume = db.Column(db.String(255), nullable=False)
    prenume = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    parola = db.Column(db.String(255), nullable=False, server_default='')
    status = db.Column(db.String(255), nullable=False)

    def __init__(self, nume, prenume, email):
        self.nume = nume
        self.prenume = prenume
        self.email = email
        self.password = ''
        self.status = ''

    def __repr__(self):
        return '<Medic {}>'.format(self.email)

    def set_password(self, parola):
        self.parola = generate_password_hash(parola)

    def set_status(self, status):
        self.status = status

    def check_password(self, parola):
        return check_password_hash(self.parola, parola)

