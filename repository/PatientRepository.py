import os

from flask import redirect, url_for
from flask_login import current_user
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model.Patient import Patient
from model.Result import Result
from repository.IRepository import IRepository
from utils.extensions import db

APP_ROOT = os.path.join('static', 'animals')
APP_ROOT6 = os.path.join('static', 'js')


class PatientRepository(IRepository):

    def __init__(self):
        pass

    def home1(self):
        return redirect(url_for('patient.pag_pacient'))

    def creeaza_pacient(self, numeP, numeC, prenumeP, prenumeC, e, tele, var, idM, paro):
        pac = Patient(numeParinte=numeP, numeCopil=numeC
                      , prenumeParinte=prenumeP
                      , prenumeCopil=prenumeC,
                      email=e, telefon=tele, varsta=var
                      , idMedic=idM)
        pac.set_password(paro)
        pac.set_status("activ")
        db.session.add(pac)
        db.session.commit()

    def toti(self):
        pacienti = Patient.query.filter_by(medicId=current_user.id).all()
        data = []

        for pacient in pacienti:
            data.append(pacient)
        return data

    def sterge(self, id):
        Patient.query.filter_by(id=id).delete()
        db.session.commit()




    def modifica_varsta(self, pacientId, var):
        pacient = Patient.query.filter_by(id=pacientId).first()

        pacient.varsta = int(var)
        db.session.commit()

    def results(self,pacientId):
        results = db.session.execute("select * from pacienti  join results on pacienti.id = :name", {"name": pacientId})
        data = []
        print("bfsjkbfjksnfs")
        for result in results:
            data.append(result)

        return data

    def graph(self,pacientId):
        results = db.session.execute("select results from results  where results.id = :name", {"name": pacientId})
        data = []

        for result in results:
            data.append(result)

        return data

patientRepository = PatientRepository()
