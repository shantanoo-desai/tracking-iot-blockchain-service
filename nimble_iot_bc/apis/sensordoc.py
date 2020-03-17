import logging
# from collections import OrderedDict
from flask_restplus import Namespace, Resource, fields, reqparse

from nimble_iot_bc.databases.sensordb import influx

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# API Namespace for Sensor Document
api = Namespace('sensordoc', description='Sensor Document Operations')

request_parser = reqparse.RequestParser()

request_parser.add_argument(
    'hash',
    required=True,
    type=str
)


# API Models for Sensor Document
sensor = api.model('sensor', {
        'ID': fields.String(required=True, description='Sensor\'s MAC Address'),
        'make': fields.String(required=True, description='Type of Sensor')
})

measurement = api.model('measurement', {
        'timestamp': fields.String(required=True, description='UTC Timestamp of Measured Values'),
        'humid': fields.Float(required=True, description='% Relative Humidity Value'),
        'temp': fields.Float(required=True, description='Temperature Value in °C')
})

sensor_doc = api.model('SensorDoc', {
    'bizLocation': fields.String(required=True, description='EPCIS Business Location Code'),
    'sensor': fields.Nested(sensor),
    'measurement': fields.Nested(measurement)
})


def create_sensor_doc(datapoints):
    """Generate a JSONic Sensor Document based on given a list of datapoints

    :param: datapoints: a list of data points from Sensor DB
    :type: list of dictionaries from Sensor DB's query ResultSet
    :returns: sensor_doc_to_send: list of formatted data
    :rtype: list
    """
    """Document Format:
        [
            {
                'bizLocation': <str>,
                'sensor': {
                    'ID': <str>,
                    'make': <str>
                },
                'measurement': {
                        'timestamp': <rfc3339_str>,
                        'humid': <float>,
                        'temp': <float>
                }
            }
        ]
    """
    # sensor_doc_to_send = []
    for point in datapoints:
        _sub_doc = {
            'bizLocation': point['bizLocation'],
            'sensor': {
                'ID': point['sID'],
                'make': point['sName']
            },
            'measurement': {
                'timestamp': point['time'],
                'humid': point['humid'],
                'temp': point['temp']
            }
        }
        yield _sub_doc


# API Routes

@api.route('')
@api.doc(
    params={
        'hash': 'SHA256 Hash String. \
        e.g. `5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03`'
    },
    responses={
        400: 'Given Hash is Incorrect'
    }
)
class SensorDocResource(Resource):
    @api.expect(request_parser)
    @api.marshal_list_with(sensor_doc)
    def get(self):
        '''
        Fetch a Sensor Document given its SHA-256 Hash
        '''
        logger.info('sensordoc: called')
        # parse the incoming hash in the request
        args = request_parser.parse_args()
        incoming_hash = args.get('hash')

        if len(incoming_hash) == 64:
            query = 'SELECT * FROM env WHERE hash=\'{}\''.format(incoming_hash)
            logger.debug('InfluxDB Query: {}'.format(query))

            results = list(influx.connect().query(query))
            logger.debug('No. of Datapoints from InfluxDB Query: {}'.format(
                len(results)
            ))

            if len(results):
                logger.info('Creating Sensor Doc for Datapoints')
                response = create_sensor_doc(results[0])
                return list(response)

            else:
                logger.info('No Datapoints available for given InfluxDB Query')
                return []  # return empty list under HTTP 200

        else:
            logger.info('incoming hash length {} is not standard SHA-256 hash'.format(
                len(incoming_hash)))
            api.abort(400, 'Given Hash is not SHA-256 length compliant')
