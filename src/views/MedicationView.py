from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.MedicationModel import MedicationModel, MedicationSchema
from ..models.ReviewModel import ReviewModel, ReviewSchema

medication_api = Blueprint('medication_api', __name__)
medication_schema = MedicationSchema()
review_schema = ReviewSchema()


@medication_api.route('/', methods=["POST"])
@Auth.auth_required
def create_medication():

    rec_data = request.get_json()
    rec_data['patient_id'] = g.user.get('id')
    medication_data = medication_schema.load(rec_data)
    medication = MedicationModel(medication_data)
    medication.save()
    medication_data_final = medication_schema.dump(medication)
    return custom_response(medication_data_final, 201)


@medication_api.route('/<int:medication_id>/reviews', methods=['POST'])
@Auth.auth_required
def medication_review(medication_id):
    rec_data = request.get_json()
    rec_data['patient_id'] = g.user.get('id')
    rec_data['medication_id'] = medication_id

    if not rec_data.get('review_content'):
        return custom_response({'error': 'No review passed'}, 400)

    if rec_data['patient_id'] and rec_data['medication_id']:
        review_data = review_schema.load(rec_data)
        review_data_upload = ReviewModel(review_data)
        review_data_upload.save()
        return custom_response({'message': 'Review has been added'}, 200)
    else:
        return custom_response({'error': 'Invalid request'}, 400)


# @medication_api.route('/<int:medication_id>/reviews', methods=['PUT'])
# @Auth.auth_required
# def update_medication(medication_id):
#     _data = request.get_json()
#     medication_data['patient_id'] = g.user.get('id')
#     # medication = MedicationModel.get_one_medication(medication_id)
#     medication_data['medication_id'] = medication_id
#
#     if not medication_data.get('review_content'):
#         return custom_response({'error': 'No review passed'}, 400)
#
#     if medication_data['patient_id'] and medication_data['medication_id']:
#         #return custom_response({'error': 'Login to leave a review'}, 404)
#
#     medication_upload = review_schema.load(medication_data, partial=True)
#     medication_upload2 = ReviewModel
#     medication.update(medication_upload)
#
#     medication_dump = medication_schema.dump(medication)
#     return custom_response(medication_dump, 200)


@medication_api.route('/<int:medication_id>/reviews', methods=['PUT'])
@Auth.auth_required
def update_medication_review(medication_id):
    review_data = request.get_json()
    review_data['patient_id'] = g.user.get('id')
    review_data['medication_id'] = medication_id
    review = ReviewModel.get_one_review(medication_id)

    if not review_data.get('review_content'):
        return custom_response({'error': 'No review edit passed'}, 400)

    if review_data['patient_id'] and review_data['medication_id']:
        review_edit = review_schema.load(review_data, partial=True)
        review.update(review_edit)
        review_dump = review_schema.dump(review)
        return custom_response(review_dump, 200)
    else:
        return custom_response({'error': 'Invalid request'}, 400)


@medication_api.route('/<int:review_id>/reviews', methods=['DELETE'])
@Auth.auth_required
def delete_review(review_id):

    review_data = ReviewModel.get_one_review(review_id)

    if not review_data:
        return custom_response({'error': 'recipe not found'}, 404)

    review = review_schema.dump(review_data)
    if review.get('patient_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    review_data.delete()
    return custom_response({'message': 'deleted'}, 204)


@medication_api.route('/<int:review_id>/reviews', methods=['GET'])
@Auth.auth_required
def get_one_review(review_id):
    review_data = ReviewModel.get_one_review(review_id)
    if not review_data:
        return custom_response({'error': 'recipe not found'}, 404)
    review = review_schema.dump(review_data)
    return custom_response(review, 200)


@medication_api.route('/reviews', methods=['GET'])
@Auth.auth_required
def get_all_reviews():
    review_all = ReviewModel.query
    review_all = review_all.all()
    review = review_schema.dump(review_all, many=True)
    return custom_response(review, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )