import logging
from flask_restplus import Namespace, Resource, fields, reqparse

from databases.documentdb import mongo

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# API Namespace for Hash Document
api = Namespace('hashdoc', description='IoT-EPC-Event Hash Document Operations')

# Request Parser
event_duration_parser = reqparse.RequestParser()
event_duration_parser.add_argument(
    'from',
    type=str,
    required=False,
    help='UTC Timestamp of previous Event e.g. `2019-01-01T10:45:10.800Z`')

event_duration_parser.add_argument(
    'to',
    type=str,
    required=False,
    help='UTC Timestamp of present Event. e.g. `2019-01-01T10:50:15.900Z`')


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

@api.route('/')
@api.doc(responses={404: 'No Hash Documents Exist'})
class HashDocDumpResource(Resource):
    @api.marshal_list_with(hash_doc)
    def get(self):
        '''
        Fetch All IoT-EPC Event Hash Documents
        '''
        logger.info('hashdoc/ API: called')
        projection = {'_id': 0}

        all_hash_docs = mongo.db['HashData'].find(
                                {},
                                projection)
        list_hash_docs = list(all_hash_docs)

        if len(list_hash_docs):
            return list_hash_docs

        else:
            logger.info('hashdoc/ API: No Data found')
            return api.abort(404)


@api.route('/<string:product_id>')
@api.param('product_id', 'EPC Product ID')
@api.doc(responses={404: 'No Values Exist for given Product ID'})
class HashDocResource(Resource):
    @api.expect(event_duration_parser)
    @api.marshal_list_with(hash_doc)
    def get(self, product_id):
        '''
        Fetch IoT-EPC Event Hash Documents for given EPC Product ID & Time Duration (if provided).
        '''
        args = event_duration_parser.parse_args()
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

        logger.info('hashdoc/{}: called'.format(product_id))

        product_hash_doc = mongo.db['HashData'].find(
                                    query,
                                    projection)
        list_product_hashdoc = list(product_hash_doc)

        if len(list_product_hashdoc):
            logger.debug('No. of Product Hash Documents found: {}'.format(
                str(
                    len(list_product_hashdoc))
                )
            )
            return list_product_hashdoc

        else:
            logger.info('No Product Hash Documents found')
            api.abort(404, 'No Values Exist for Product ID {}'.format(product_id))
