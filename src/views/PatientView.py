from flask import request, json, Response, Blueprint, g
from ..models.PatientModel import PatientModel, PatientSchema
from ..shared.Authentication import Auth

patient_api = Blueprint('patient_api', __name__)
patient_schema = PatientSchema()


@patient_api.route('/signup', methods=['POST'])
def create():

    req_data = request.get_json()
    data = patient_schema.load(req_data, partial=True)
    patient_in_db = PatientModel.get_patient_by_email(data.get('email'))

    if patient_in_db:
        message = {'error': "Patient already exists, please add another email"}
        return custom_response(message, 400)

    patient = PatientModel(data)
    patient.save()
    patient_data = patient_schema.dump(patient)

    token = Auth.generate_token(patient_data.get('id'))
    return custom_response({'jwt_token': token}, 201)


@patient_api.route('/signin', methods=['POST'])
def signin():

    signin_data = request.get_json()

    data = patient_schema.load(signin_data, partial=True)

    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'Email required to signin'}, 400)

    patient = PatientModel.get_patient_by_email(data.get('email'))

    if not patient:
        return custom_response({'error': 'Invald Login Credentials'}, 400)

    if not patient.check_hash(data.get('password')):
        return custom_response({'error': 'Enter the correct password'}, 400)

    correct_sign_in = patient_schema.dump(patient)
    token = Auth.generate_token(correct_sign_in.get('id'))

    return custom_response({'jwt_token': token}, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
        """
    return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
    )
