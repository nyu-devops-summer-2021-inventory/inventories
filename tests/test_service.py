"""
InventoryItem API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN

  While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_service.py:TestInventoryItemServer
"""

import os
import logging
import unittest

# from unittest.mock import MagicMock, patch
from urllib.parse import quote_plus
from service import status  # HTTP Status Codes
from service.models import db, init_db
from service.routes import app
from .factories import InventoryItemFactory

# Disable all but ciritcal errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/inventories"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestInventoryItemServer(unittest.TestCase):
    """InventoryItem Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_index(self):
        """
        Test the index page
        Return some useful information when root url is requested
        """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], 'Inventory Service')

    def test_create_inventory_item(self):
        """Create a new Inventory item"""
        test_inventory_item = InventoryItemFactory()
        logging.debug(test_inventory_item)
        resp = self.app.post(
            BASE_URL,
            json=test_inventory_item.serialize(),
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_inventory_item = resp.get_json()
        self.assertEqual(
            new_inventory_item["sku"], test_inventory_item.sku, "Names do not match"
        )

    def test_update_in_stock(self):
        """Update in stock status for an inventory item"""
        # TODO: create an inventory to update
        test_inventory_item = InventoryItemFactory()
        resp = self.app.post(
            BASE_URL,
            json=test_inventory_item.serialize(),
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the pet
        new_inventory_item = resp.get_json()
        logging.debug(new_inventory_item)
        new_inventory_item["in_stock"] = False
        resp = self.app.put(
            "/inventories/{}/in-stock".format(new_inventory_item["id"]),
            json=new_inventory_item,
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_inventory_item = resp.get_json()
        self.assertEqual(updated_inventory_item["in_stock"], False)
