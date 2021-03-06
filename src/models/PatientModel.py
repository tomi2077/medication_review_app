from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from .ReviewModel import ReviewSchema


class PatientModel(db.Model):

    __table__name = 'patients'
    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String(128), nullable=False)
    email = db.column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullabe=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    reviews = db.relationship('ReviewModel', backref='reviews', lazy=True)

    def __init__(self, data):

        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
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
    def get_all_patients():
        return PatientModel.query.all()

    @staticmethod
    def get_one_patient():
        return PatientModel.query.get(id)

    @staticmethod
    def get_patient_by_email(value):
        return PatientModel.query.filter_by(email=value).first()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode('utf-8')

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr(self):
        return '<id {}>'.format(self.id)


class PatientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    reviews = fields.Nested(ReviewSchema, many=True)








