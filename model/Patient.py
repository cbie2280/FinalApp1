from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from utils.extensions import db


class Patient(UserMixin, db.Model):
    __tablename__ = 'pacienti'
    id = db.Column(db.Integer(), primary_key=True)
    numeParinte = db.Column(db.String(255), nullable=False)
    prenumeParinte = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    telefon = db.Column(db.Integer, nullable=False)
    parola = db.Column(db.String(255), nullable=False, server_default='')
    numeCopil = db.Column(db.String(255), nullable=False)
    prenumeCopil = db.Column(db.String(255), nullable=False)
    varsta = db.Column(db.Integer, nullable=False)
    medicId = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(255), nullable=False)

    def __init__(self, numeParinte, numeCopil, prenumeParinte, prenumeCopil, email, telefon, varsta, idMedic):
        self.numeParinte = numeParinte
        self.numeCopil = numeCopil
        self.prenumeParinte = prenumeParinte
        self.prenumeCopil = prenumeCopil
        self.telefon = telefon
        self.email = email
        self.varsta = varsta
        self.password = ''
        self.status = ''
        self.medicId = idMedic

    def __repr__(self):
        return '<Pacient {}>'.format(self.email)

    def set_password(self, parola):
        self.parola = generate_password_hash(parola)

    def set_varsta(self, v):
        self.varsta = generate_password_hash(v)

    def set_status(self, status):
        self.status = status

    def check_password(self, parola):
        return check_password_hash(self.parola, parola)
