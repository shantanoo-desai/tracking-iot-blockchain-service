import os
import logging
import urllib.parse
from flask import Flask, Blueprint
from flask_cors import CORS
from apis import api
from databases import mongo, influx

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def configure_app(flask_app):
    # Flask-Restplus Swagger Configuration
    logger.info('Configuring Flask App')
    flask_app.config.from_envvar('APP_CONFIG')

def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    flask_app.register_blueprint(blueprint)

    # Databases (Mongo, InfluxDB)
    mongo.init_app(flask_app)
    influx.init_app(flask_app)

def main():
    logger.info('Starting Server for IoT-Blockchain API')
    initialize_app(app)
    app.run(debug=False, host='0.0.0.0')

if __name__ == "__main__":
    main()
