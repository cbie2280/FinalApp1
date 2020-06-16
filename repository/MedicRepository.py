from model.Medic import Medic
from repository.IRepository import IRepository
from utils.extensions import db


class MedicRepository(IRepository):

    def __init__(self):
        pass

    def toti(self):
        medici = Medic.query.all()
        data = []

        for medic in medici:
            data.append(medic)
        return data

    def sterge(self, id):
        Medic.query.filter_by(id=id).delete()
        db.session.commit()

    def aproba_medic(self, medicId):
        medic = Medic.query.filter_by(id=medicId).first()

        medic.status = "activ"
        db.session.commit()


medicRepository = MedicRepository()
