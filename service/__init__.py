"""
Package: service
Package for the application models and service routes
"""
import logging
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

# Create Flask application
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accounts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"

# Set up logging
app.logger.setLevel(logging.INFO)
app.logger.info("Service initialized...")

# Set up Talisman security headers
talisman = Talisman(app, force_https=False)

# Set up CORS policies
CORS(app)

from service.models import db  # noqa: E402
db.init_app(app)

from service import routes  # noqa: F401, E402
