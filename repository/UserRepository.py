from flask import flash
from flask_login import login_user, logout_user

from model.Medic import Medic
from model.Patient import Patient
from utils.extensions import db


class UserRepository:
    def __init__(self):
        pass

    def login(self, e, passw, rememb):

        email = Medic.query.filter_by(email=e).first()

        if e == "admin@yahoo.com" and passw == "passw":
            print(e)
            print(passw)
            return 3

        if email is None or not email.check_password(passw):
            email1 = Patient.query.filter_by(email=e).first()

            if email1 is None or not email1.check_password(passw):

                return 0

            login_user(email1, remember=rememb)

            return 1

        login_user(email, remember=rememb)
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('medic.home')
        return 2

    def logout(self):
        logout_user()


    def register(self, n, p, e, par):

        medic = Medic(nume=n, prenume=p, email=e)
        medic.set_password(par)
        medic.set_status("verifică")
        db.session.add(medic)
        db.session.commit()
        flash('Felicitari, acum ai cont!')



generalRepository = UserRepository()
