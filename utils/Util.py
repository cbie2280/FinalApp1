from model.Medic import Medic
from model.Patient import Patient

from app import login
from utils.extensions import db

@login.user_loader
def load_user(id):
    if Medic.query.get(int(id)) is not None:
        return Medic.query.get(int(id))
    if Patient.query.get(int(id)) is not None:
        return Patient.query.get(int(id))
    return None
