from flask import Blueprint
from flask_login import login_required

from controller.MedicController import medicController

mod1 = Blueprint("medic", __name__)


@mod1.route('/')
@mod1.route('/home')
@login_required
def home():
    return medicController.home()


@mod1.route('/pag_medic', methods=['GET', 'POST'])
@login_required
def pag_medic():
    return medicController.pag_medic()


@mod1.route('/toti_medicii', methods=['GET'])
# @login_required
def toti_medicii():

    return medicController.toti()


@mod1.route('/sterge_medic/<medicId>')
# @login_required
def sterge_medic(medicId):
    return medicController.sterge(medicId)


@mod1.route('/aproba_medic/<medicId>', methods=['GET', 'POST'])
# @login_required
def aproba_medic(medicId):
    return medicController.aproba_medic(medicId)