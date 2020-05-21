from marshmallow import fields, Schema
import datetime
from . import db
from .PatientModel import PatientSchema
from .ReviewModel import ReviewSchema


class MedicationModel(db.Model):

    __table__name = 'medications'
    id = db.column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    reviews = db.relationship('ReviewModel', backref='reviews', lazy=True)

    def __init__(self, data):

        self.content = data.get('content')
        self.patient_id = data.get('patient_id')
        self.created_at = data.get('created_at')
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.generate_hash(item)
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_medications():
        return MedicationModel.query.all()

    @staticmethod
    def get_one_medication():
        return MedicationModel.query.get(id)

    @staticmethod
    def get_patients_medications(patient_id):
        return MedicationModel.query.filter_by(patient_id=patient_id)

    def __repr(self):
        return '<id {}>'.format(self.id)


class MedicationSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    patient_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)






