# TODO: Copyright header

"""
Package for the application models and service routes for the inventory service

This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
import logging
from flask import Flask

# Create Flask application
app = Flask(__name__)
app.config.from_object("config")

# Import the models after the Flask app is created
# TODO: Also import routes and error handlers
from service import models

# Set up logging for production
print("Configuring logging for {}...".format(__name__))
app.logger.propagate = False

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    # Make all log formats consistent
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", 
        "%Y-%m-%d %H:%M:%S %z"
    )

    for handler in app.logger.handlers:
        handler.setFormatter(formatter)
        
    app.logger.info("Logging handler established")

app.logger.info(70 * "*")
app.logger.info("  I N V E N T O R Y   S E R V I C E  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make our sqlalchemy tables
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

app.logger.info("Service inititalized!")
