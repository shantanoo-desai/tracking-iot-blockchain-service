import logging
import json
import hashlib
import requests
from flask_restplus import Namespace, Resource, fields, reqparse
from databases.sensordb import influx
from databases.documentdb import mongo
from apis.sensordoc import create_sensor_doc

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# API Namespace for Verification
api = Namespace('verify', description='Verify if IoT data is stored in Blockchain as well \
                as checked for Track&Trace')

# Request Parser for Time Duration
event_duration_parser = reqparse.RequestParser()
event_duration_parser.add_argument(
    'productID',
    type=str,
    required=True
)

event_duration_parser.add_argument(
    'from',
    type=str,
    required=True
)

event_duration_parser.add_argument(
    'to',
    type=str,
    required=True
)

# Model for verification (simple boolean model)
verified_response = api.model('Validation', {
    'validated': fields.Boolean(required=True)
})


def check_data_integrity(incoming_hash):
    """Check Data Integrity of the Hash by comparing it Sensor Document Queried
       via Sensor DB. If the incoming hash and the generated hash are the same,
       no data has been tampered with, hence data integrity is maintained.

    :param: incoming_hash: SHA-256 string from Document DB
    :type: SHA-256 Hash from Document DB
    :returns: dict: {'checked': True, 'hash': generated_sha256_hash}
    :rtype: dict
    """

    influx_query = 'SELECT * FROM env WHERE hash=\'{}\''.format(incoming_hash)
    logger.debug('check_data_integrity: InfluxDB Query: {}'.format(influx_query))

    results = list(influx.connect().query(influx_query))
    logger.debug('check_data_integrity: No. of Data Points {}'.format(len(results)))

    if len(results):

        logger.info('check_data_integrity: Creating Sensor Document for Datapoints')
        created_sensor_doc = create_sensor_doc(results[0])

        logger.info('check_data_integrity: Generating SHA-256 hash for Sensor Document')
        generated_hash = hashlib.sha256(json.dumps(created_sensor_doc).encode('utf-8')).hexdigest()
        logger.debug('check_data_integrity: Generated hash: {}'.format(generated_hash))

        if generated_hash == incoming_hash:
            return {'checked': True, 'hash': generated_hash}

        else:
            return {'checked': False, 'hash': generated_hash}
    else:
        return {'checked': False, 'hash': None}


def check_in_blockchain(incoming_hash):
    """Check if the SHA-256 stored in the Document DB exists in the Blockchain network.

    :param: incoming_hash: SHA-256 string from Document DB
    :type: SHA-256 Hash from Document DB
    :returns: dict: {'exists': True}
    :rtype: dict
    """
    key_value_for_api = 'sensor,' + incoming_hash
    params_for_api = {'hash': key_value_for_api}

    # Currently this Endpoint Is fixed
    response_from_bc = requests.get('http://161.156.70.125:5000/hash', params=params_for_api)

    if response_from_bc.status_code == 200:
        result_bc = response_from_bc.json()
        print(result_bc['message'])
        return {'exists': True}

    else:
        return {'exists': False}


# API Routes
@api.route('')
@api.doc(
    params={
        "productID": "product's EPC ID",
        "from": "UTC Timestamp of present Event. e.g. `2019-01-01T10:50:15.900Z`",
        "to": "UTC Timestamp of Present EPC Event. e.g. `2019-01-01T10:50:15.900Z`"
    },
    responses={
            404: 'No Data Exists for Given Product ID and Time Range'
    }
)
class VerifyResource(Resource):
    @api.expect(event_duration_parser, validate=True)
    @api.marshal_with(verified_response)
    def get(self):
        '''
            API for frontend-service to cross-check a product's IoT Data Integrity with Blockchain
        '''
        args = event_duration_parser.parse_args()
        product_id = args.get('productID')
        from_time = args.get('from')
        to_time = args.get('to')

        query = {'epc': product_id}
        projection = {'_id': 0}

        if from_time and to_time:
            logger.info('verify/{}&from={}&to={}: called'.format(product_id, from_time, to_time))
            query['event.from_time'] = from_time
            query['event.to_time'] = to_time

        logger.info('verify/{}: called'.format(product_id))
        product_hash_doc = mongo.db['HashData'].find(
                                    query,
                                    projection)

        list_product_hash_doc = list(product_hash_doc)
        logger.debug('No. of Product Hash Document(s):{}'.format(len(list_product_hash_doc)))

        if len(list_product_hash_doc):
            logger.debug('Sensor Hash from Document: {}'.format(
                list_product_hash_doc[0]['sensor']['hash']))

            logger.info('Checking if Hash exists in Blockchain Network')
            check_hash_in_bc = check_in_blockchain(
                list_product_hash_doc[0]['sensor']['hash'])

            if check_hash_in_bc['exists']:
                logger.info('Hash exists in Blockchain Network')
                logger.info('Checking Data Integrity of IoT Data with Blockchain')

                cross_validate_iot_data = check_data_integrity(
                    list_product_hash_doc[0]['sensor']['hash'])

                # check if data integrity is intact
                if cross_validate_iot_data['checked']:
                    logger.info('Integrity Validated')
                    # data is thoroughly validated
                    return {'validated': True}
            # Hash doesn't exist in Blockchain
            logger.info('Hash does not exist in Blockchain Network')
            return {'validated': False}

        else:
            logger.info('No Data for given Product and Time Range')
            return {'validated': False}  # return False value if nothing exists
