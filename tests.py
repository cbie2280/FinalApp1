import unittest


from app import create_app
from utils.extensions import db
from model.Medic import Medic
from model.Patient import Patient


class TestBase(unittest.TestCase):

    def create_app(self):

        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='postgresql://postgres:bobby24@localhost:5433/testing'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        with create_app('testing').app_context():
            db.create_all()


    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestModels(TestBase):
    def test_add_medic(self):


        medic = Medic("test", "test", "test")
        medic.set_password("test")


        db.session.add(medic)
        db.session.commit()

        self.assertEqual(Medic.query.count(), 1)


    def test_modify_medic(self):


        medic = Medic("test", "test", "test")
        medic.set_password("123")


        db.session.add(medic)
        db.session.commit()

        update = Medic.query.filter(Medic.status=='test')
        update.username = "status"
        db.session.commit()

        self.assertEqual(Medic.query.filter(Medic.username=='status'), 1)

    def test_add_patient(self):


        patient = Patient("numeParinte", "numeCopil", "prenumeParinte", "prenumeCopil", "email", "telefon", "varsta", "idMedic")
        patient.set_password("pass")

        db.session.add(patient)
        db.session.commit()

        self.assertEqual(Patient.query.count(), 1)

    def test_delete_patient(self):
        patient = Patient("numeParinte", "numeCopil", "prenumeParinte", "prenumeCopil", "email", "telefon", "varsta",
                          "idMedic")
        patient.set_password("pass")


        db.session.add(patient)
        db.session.commit()

        delete = Patient.query.filter(Patient.medicId == 'idMedic')
        db.session.delete(delete)
        db.session.commit()

        self.assertEqual(Patient.query.count(), 0)

    def test_modify_patient(self):
        patient = Patient("numeParinte", "numeCopil", "prenumeParinte", "prenumeCopil", "email", "telefon",
                              "varsta",
                              "idMedic")
        patient.set_password("pass")

        db.session.add(patient)
        db.session.commit()

        update = Medic.query.filter(Patient.varsta == '100')
        update.username = "100"
        db.session.commit()

        self.assertEqual(Medic.query.filter(Medic.username == 'status'), 1)

if __name__ == '__main__':
    unittest.main()