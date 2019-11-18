# Main API Declaration for IoT-Blockchain API
# All different Namespaces for the App are imported here

from flask_restplus import Api

from .sensordoc import api as sensordoc_ns
from .hashdoc import api as hashdoc_ns
from .verification import api as verification_ns

api = Api(
    title='IoT-Blockchain API',
    version='1.1',
    description='IoT Data and Blockchain related Information for NIMBLE Platform Track&Trace'
)

api.add_namespace(sensordoc_ns)
api.add_namespace(hashdoc_ns)
api.add_namespace(verification_ns)
