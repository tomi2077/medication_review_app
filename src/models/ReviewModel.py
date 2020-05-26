from marshmallow import fields, Schema
import datetime
from . import db


class ReviewModel(db.Model):

    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review_content = db.Column(db.String(1000), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):

        self.review_content = data.get('review_content')
        self.patient_id = data.get('patient_id')
        self.medication_id = data.get('medication_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

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
    def get_all_reviews():
        return ReviewModel.query.all()

    @staticmethod
    def get_one_review(id):
        return ReviewModel.query.get(id)

    @staticmethod
    def get_medications_reviews(medication_id):
        return ReviewModel.query.filter_by(medication_id=medication_id)

    def __repr(self):
        return '<id {}>'.format(self.id)


class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    review_content = fields.Str(required=True)
    patient_id = fields.Int(required=True)
    medication_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)





