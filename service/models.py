# TODO: Add a license header

"""
Models for the inventory service

Models
------
InventoryItem - An item stored in the inventory service
"""
from enum import Enum
import logging
from typing import Dict, Union

from flask import app, Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    """Initialies the SQLAlchemy app"""
    InventoryItem.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""

    pass


class Condition(Enum):
    """Enumeration of valid Item conditions"""

    New = 0
    Used = 1
    OpenBox = 2


class InventoryItem(db.Model):
    """Class that represents an Item contained within our inventory"""

    app = None

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(63), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    condition = db.Column(
        db.Enum(Condition), 
        nullable=False, 
        server_default=(Condition.New.name),
    )
    restock_level = db.Column(db.Integer, nullable=False)
    restock_amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Inventory item {self.sku} id={self.id}>"

    def serialize(self) -> Dict[str, Union[str, int]]:
        """Serialize an InventoryItem into a dictionary"""
        return {
            "id": self.id,
            "sku": self.sku,
            "count": self.count,
            "condition": self.condition.name,
            "restock_level": self.restock_level,
            "restock_amount": self.restock_amount,
        }

    def deserialize(self, data: Dict[str, Union[str, int]]):
        """Deserialize an inventory item from a dictionary"""
        try:
            self.sku = data["sku"]
            self.count = data["count"]
            self.condition = getattr(Condition, data["condition"])
            self.restock_level = data["restock_level"]
            self.restock_amount = data["restock_amount"]
        except KeyError as error:
            raise DataValidationError(
                f"Invalid inventory item: missing {error.args[0]}"
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid inventory item: request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app: Flask):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # Initialize from our Flask app
        db.init_app(app)
        app.app_context().push()
        # Create tables
        db.create_all()
