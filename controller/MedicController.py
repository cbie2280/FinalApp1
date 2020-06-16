from flask import render_template, redirect, url_for

from controller.IController import IController
from repository.MedicRepository import medicRepository, MedicRepository


class MedicController(IController):

    def __init__(self,):
        pass

    def home(self):
        return redirect(url_for('medic.pag_medic'))

    def pag_medic(self):
        return render_template('pag_medic.html')

    def toti(self):

        data = medicRepository.toti()
        return render_template('toti_medicii.html', title='Medici', value=data)

    def sterge(self, medicId):
        medicRepository.sterge(medicId)
        return redirect(url_for('medic.toti_medicii'))

    def aproba_medic(self, medicId):
        medicRepository.aproba_medic(medicId)
        return redirect(url_for('medic.toti_medicii'))


medicController = MedicController()
