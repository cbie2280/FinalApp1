from sqlalchemy import Float

from utils.extensions import db


class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    results = db.Column(db.ARRAY(Float), nullable=False)
    mean = db.Column(db.Float, nullable=False)
    pacientId = db.Column(db.Float, nullable=False)

    def __init__(self, date, results, mean, pacientId):
        self.date = date
        self.results = results
        self.mean = mean
        self.pacientId=pacientId
