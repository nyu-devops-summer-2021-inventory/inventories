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

from flask import Flask
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
    in_stock = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f"<Inventory item {self.sku} id={self.id}>"

    def create(self):
        """
        Creates an Inventory item to the database
        """
        logger.info("Creating %s", self.sku)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates an Inventory item to the database
        """
        logger.info(
            "Saving %s", self.sku
        )  # TODO: Not sure about the sku part. Might change it later.
        if not self.id:
            raise DataValidationError("Update called with empty ID field.")
        db.session.commit()

    def serialize(self) -> Dict[str, Union[str, int]]:
        """Serialize an InventoryItem into a dictionary"""
        return {
            "id": self.id,
            "sku": self.sku,
            "count": self.count,
            "condition": self.condition.name,
            "restock_level": self.restock_level,
            "restock_amount": self.restock_amount,
            "in_stock": self.in_stock,
        }

    def deserialize(self, data: Dict[str, Union[str, int]]):
        """Deserialize an inventory item from a dictionary"""
        try:
            self.sku = data["sku"]
            self.count = data["count"]
            self.condition = getattr(Condition, data["condition"])
            self.restock_level = data["restock_level"]
            self.restock_amount = data["restock_amount"]
            self.in_stock = data["in_stock"]
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

    @classmethod
    def find(cls, inventory_item_id):
        """Finds an inventory item by it's ID

        :param inventory_item_id: the id of the inventory item to find
        :type inventory_item_id: int

        :return: an instance with the inventory_item_id, or None if not found
        :rtype: InventoryItem

        """
        logger.info("Processing lookup for id %s ...", inventory_item_id)
        return cls.query.get(inventory_item_id)
