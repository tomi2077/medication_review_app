from flask import Flask
from .config import app_config
from .models import db, bcrypt

from .views.PatientView import patient_api as patient_blueprint
from .views.MedicationView import medication_api as medication_blueprint


def create_app(env_name):

    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)

    db.init_app(app)

    app.register_blueprint(patient_blueprint, url_prefix='/api/v1/patients')
    app.register_blueprint(medication_blueprint, url_prefix='/api/v1/medications')

    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return 'Congratulations! Your first endpoint is working'

    return app
