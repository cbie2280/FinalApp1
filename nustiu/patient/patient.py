import json
from datetime import datetime, time
from random import random
from flask import Flask, render_template, jsonify, request, make_response

from flask import Blueprint, Response, render_template
from flask_login import login_required

from flask import Flask, render_template, jsonify, request

from controller.PatientController import patientController
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure



mod2 = Blueprint("patient", __name__)


@mod2.route('/')
@mod2.route('/home1')
@login_required
def home1():
    return patientController.home1()


@mod2.route('/creeaza_pacient', methods=['GET', 'POST'])
@login_required
def creeaza_pacient():
    return patientController.creeaza_pacient()


@mod2.route('/pag_pacient', methods=['GET', 'POST'])
@login_required
def pag_pacient():
    return patientController.pag_pacient()


@mod2.route('/toti_pacientii', methods=['GET'])
@login_required
def toti_pacientii():

    return patientController.toti()


@mod2.route('/sterge_pacient/<pacientId>')
@login_required
def sterge_pacient(pacientId):
    return patientController.sterge(pacientId)



@mod2.route('/modifica_varsta/<pacientId>', methods=['GET', 'POST'])
@login_required
def modifica_varsta(pacientId):
    print("bla")
    return patientController.modifica_varsta(pacientId)



@mod2.route('/results/<pacientId>', methods=["GET", "POST"])
def results(pacientId):
    return patientController.results(pacientId)

