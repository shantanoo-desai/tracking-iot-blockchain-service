import logging
from flask import Flask
from flask_cors import CORS
from nimble_iot_bc.apis import blueprint as api
from nimble_iot_bc.databases import mongo, influx

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

main_app = Flask(__name__)


def configure_app(flask_app):
    '''Configure the complete Flask App using a `.cfg` file
       as an environment variable
    '''

    logger.info('Configuring Flask App')
    try:
        flask_app.config.from_envvar('APP_CONFIG')
    except Exception as e:
        logger.error('No APP_CONFIG variable found. No configuration found.')
        raise(e)


def initialize_app(flask_app):
    '''Initialize the complete Flask App with a Blueprint
       and Database initializations
    '''
    configure_app(flask_app)

    # blueprint = Blueprint('api', __name__, url_prefix='/api')
    # api.init_app(blueprint)
    flask_app.register_blueprint(api, url_prefix='/api')

    # Databases (Mongo, InfluxDB)
    mongo.init_app(flask_app)
    influx.init_app(flask_app)


def main():
    '''Main function that returns the CORS-configured Flask App
    '''
    logger.info('Starting Server for IoT-Blockchain API')
    CORS(main_app)
    initialize_app(main_app)
    return main_app


def request_context():
    return main_app.app_context()


# Necessary for uWSGI Server's configuration file
entrypoint = main()

if __name__ == "__main__":
    # Always in Production Mode.
    entrypoint.run(debug=False)
