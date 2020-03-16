import logging
from flask_restplus import Namespace, Resource, fields, reqparse

from nimble_iot_bc.databases.documentdb import mongo

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# API Namespace for Hash Document
api = Namespace('hashdoc', description='IoT-EPC-Event Hash Document Operations')

# Request Parser
event_duration_parser = reqparse.RequestParser()

event_duration_parser.add_argument(
    'productID',
    type=str,
    required=True
)

event_duration_parser.add_argument(
    'from',
    type=str,
    required=False
)

event_duration_parser.add_argument(
    'to',
    type=str,
    required=False
)


# Models for Hash Document
bizLocations = api.model('bizLocations', {
    'prev': fields.String(required=True, description='Previous EPC Business Location'),
    'present': fields.String(required=True, description='Present EPC Business Location')
})

epc_event = api.model('event', {
    'bizLocation': fields.Nested(bizLocations),
    'from_time': fields.String(
        required=False,
        description='UTC ISO8601 Timestamp from Previous Event in millisecond precision'
    ),
    'to_time': fields.String(
        required=False,
        description='UTC ISO8601 Timestamp to Present Event in millisecond precision'
    )
})

sensor_hash = api.model('sensorHash', {
    'hash': fields.String(required=True, description='SHA-256 Generated Cryptographic Hash')
})

hash_doc = api.model('HashDoc', {
    'epc': fields.String(required=True, description='EPC Product Code'),
    'sensor': fields.Nested(sensor_hash),
    'event': fields.Nested(epc_event)
})


# API Routes

@api.route('')
@api.doc(
    params={
        "productID": "Product's EPC ID",
        "from": "UTC Timestamp of previous Event e.g. `2019-01-01T10:45:10.800Z`",
        "to": "UTC Timestamp of present Event. e.g. `2019-01-01T10:50:15.900Z`"
    },
    responses={
        400: 'Missing Parameters for Query'
    }
)
class HashDocResource(Resource):
    @api.expect(event_duration_parser)
    @api.marshal_list_with(hash_doc)
    def get(self):
        '''
        Fetch IoT-EPC Event Hash Documents for given EPC Product ID & Time Duration (if provided).
        '''
        args = event_duration_parser.parse_args()
        product_id = args.get('productID')
        from_time = args.get('from')
        to_time = args.get('to')
        query = {'epc': product_id}
        projection = {'_id': 0}

        if from_time and to_time:
            logger.debug('hashdoc/{}?from="{}"&to="{}": called'.format(
                product_id,
                from_time,
                to_time))

            query['event.from_time'] = from_time
            query['event.to_time'] = to_time

        elif from_time and to_time is None:
            api.abort(400, 'Optional argument: "to" missing in query')

        elif to_time and from_time is None:
            api.abort(400, 'Optional argument: "from" missing in query')

        logger.info('hashdoc/{}: called'.format(product_id))

        product_hash_doc = mongo.db['HashData'].find(
                                    query,
                                    projection)
        list_product_hashdoc = list(product_hash_doc)

        if len(list_product_hashdoc):
            logger.debug('No. of Product Hash Documents found: {}'.format(
                    len(list_product_hashdoc)))
            return list_product_hashdoc

        else:
            logger.info('No Product Hash Documents found')
            return []  # return Empty List under HTTP 200
