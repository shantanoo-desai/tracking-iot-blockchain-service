# Main API Declaration for IoT-Blockchain API
# All different Namespaces for the App are imported here

from flask import Blueprint
from flask_restplus import Api

from nimble_iot_bc.apis.sensordoc import api as sensordoc_ns
from nimble_iot_bc.apis.hashdoc import api as hashdoc_ns
from nimble_iot_bc.apis.verification import api as verification_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='IoT-Blockchain API',
    version='1.5',
    description='IoT Data and Blockchain related Information for NIMBLE Platform Track&Trace',
    doc='/doc/',
    contact='Shantanoo Desai',
    contact_email='des@biba.uni-bremen.de',
)

api.add_namespace(sensordoc_ns)
api.add_namespace(hashdoc_ns)
api.add_namespace(verification_ns)
