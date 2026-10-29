"""
Models for Account Service
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Account(db.Model):
    """
    Class that represents an Account
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def create(self):
        """Creates an Account to the database"""
        logger.info("Creating %s", self.name)
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates an Account in the database"""
        logger.info("Updating %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes an Account from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes an Account into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None,
        }

    def deserialize(self, data):
        """Deserializes an Account from a dictionary"""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data["address"]
            self.phone_number = data.get("phone_number")
        except KeyError as error:
            raise DataValidationError(f"Invalid Account: missing {error.args[0]}") from error
        except TypeError as error:
            raise DataValidationError(f"Invalid Account: body of request contained bad data {str(error)}") from error
        return self

    @classmethod
    def all(cls):
        """Returns all of the Accounts in the database"""
        logger.info("Processing all Accounts")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds an Account by its ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return db.session.get(cls, by_id)
