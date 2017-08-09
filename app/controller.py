from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logger import create_logger

application = Flask(__name__, static_url_path='/service-registry')
application.config.from_pyfile('config.py')
db = SQLAlchemy(application)
logger = create_logger('service-registry.log')

from views import *

if __name__ == "__main__":
    logger.debug(
        "Starting service-registry at ip %s and port %s", application.config['MACHINE_IP'], application.config['MACHINE_PORT'])
    application.run(application.config['MACHINE_IP'], application.config['MACHINE_PORT'])