import base64
import os

from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits import mplot3d
import io
import numpy as np
import matplotlib.pyplot as plt
from flask import render_template, redirect, url_for, Response
from flask_login import current_user

from controller.IController import IController
from forms1.CreeazaPacientForm import CreeazaPacientForm
from forms1.ModificaVarsta import ModificaVarsta
from repository.PatientRepository import patientRepository

APP_ROOT = os.path.join('static', 'animals')
APP_ROOT6 = os.path.join('static', 'js')


class PatientController(IController):

    def __init__(self):
        pass

    def home1(self):
        return redirect(url_for('patient.pag_pacient'))

    def creeaza_pacient(self):
        form = CreeazaPacientForm()
        if form.validate_on_submit():
            patientRepository.creeaza_pacient(form.numeParinte.data, form.numeCopil.data,
                                              form.prenumePatinte.data,
                                              form.prenumeCopil.data, form.email.data, form.telefon.data,
                                              form.varsta.data, current_user.id, form.parola.data)
            return redirect(url_for('patient.creeaza_pacient'))
        else:
            return render_template('creeaza_pacient.html', form=form)

    def pag_pacient(self):
        return render_template('start.html')

    def toti(self):
        data=patientRepository.toti()

        return render_template('toti_pacintii.html', title='Pacientii mei', value=data)

    def sterge(self, pacientId):
        patientRepository.sterge(pacientId)
        return redirect(url_for('patient.toti_pacientii'))

    def rezulate(self, pacientId):
        data = patientRepository.rezulate(current_user.id)

        return render_template('rezulate.html', title='Rezulate', value=data)

    def modifica_varsta(self, pacientId):
        form = ModificaVarsta()

        if form.validate_on_submit():

            patientRepository.modifica_varsta(pacientId, form.varsta.data)
            return redirect(url_for('patient.toti_pacientii'))
        else:
            return render_template('modifica_varsta.html', title='Modifica varsta', form=form, p=pacientId)


    def results(self,pacientId):
        data=patientRepository.results(pacientId, current_user.id)
        return render_template('results.html', title='Rezultate', value=data)

    def graph(self,pacientId):
        data=patientRepository.graph(pacientId)
        x=[]
        y=[]
        for i in range(0,len(data[0][0])):
            x.append(data[0][0][i])
            y.append(i)
        img = io.BytesIO()

        plt.plot(y, x)
        plt.axis([0, len(y), 0, 1])
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        plot_url = base64.b64encode(img.getvalue()).decode()

        return '<img src="data:image/png;base64,{}">'.format(plot_url)



patientController = PatientController()



