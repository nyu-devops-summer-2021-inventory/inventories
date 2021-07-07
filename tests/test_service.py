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

from unittest.mock import patch
from urllib.parse import quote_plus
from service import status  # HTTP Status Codes
from service.models import db, init_db, DataValidationError
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

    def _create_inventory_items(self, count: int):
        """Factory method to create inventory items in bulk"""
        inventory_items = []
        for _ in range(count):
            test_inventory_item = InventoryItemFactory()
            resp = self.app.post(
                BASE_URL,
                json=test_inventory_item.serialize(),
                content_type=CONTENT_TYPE_JSON,
            )
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test inventory item",
            )
            new_inventory_item = resp.get_json()
            test_inventory_item.id = new_inventory_item["id"]
            inventory_items.append(test_inventory_item)
        return inventory_items

    def test_index(self):
        """
        Test the index page
        Return some useful information when root url is requested
        """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Inventory Service")

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

    def test_update_inventory_item(self):
        """ Update an Inventory item """
        # Create a dummy inventory item
        test_inventory_item = self._create_inventory_items(1)[0]
        # make the call
        resp = self.app.put(
            '{}/{}'.format(BASE_URL, test_inventory_item.id), 
            json=test_inventory_item.serialize(), 
            content_type=CONTENT_TYPE_JSON)
     
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # go back and get it again, need query function
        # TODO: uncomment the codes below after query function is finished
        # resp = self.app.get(
        #     '{}/{}'.format(BASE_URL, test_inventory_item.id), 
        #     content_type=CONTENT_TYPE_JSON)
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_inventory_item = resp.get_json()
        logging.debug('data = %s', updated_inventory_item)
        self.assertEqual(
            updated_inventory_item["id"], test_inventory_item.id, "ids do not match"
        )
        self.assertEqual(
            updated_inventory_item["sku"], test_inventory_item.sku, "names do not match"
        )
        self.assertEqual(
            updated_inventory_item["count"], test_inventory_item.count, "counts do not match"
        )
        self.assertEqual(
            updated_inventory_item["condition"], test_inventory_item.condition.name, "condations do not match"
        )
        self.assertEqual(
            updated_inventory_item["restock_level"], test_inventory_item.restock_level, "counts do not match"
        )
        self.assertEqual(
            updated_inventory_item["restock_amount"], test_inventory_item.restock_amount, "condations do not match"
        )
        self.assertEqual(
            updated_inventory_item["in_stock"], test_inventory_item.in_stock, "counts do not match"
        )
    
    def test_update_item_not_found(self):
        """ Update an Inventory item that doesn't exist """
        # Create a dummy inventory item
        test_inventory_item = self._create_inventory_items(1)[0]
        # make the call
        resp = self.app.put(
            '{}/{}'.format(BASE_URL, test_inventory_item.id - 111111111), 
            json=test_inventory_item.serialize(), 
            content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

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

        # update the inventory item
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

    def test_delete_inventory_item(self):
        """Delete an inventory item"""
        # Create a dummy inventory item
        test_inventory_item = self._create_inventory_items(1)[0]

        # Send a request to delete the dummy item
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_inventory_item.id),
            content_type=CONTENT_TYPE_JSON,
        )

        # Ensure the response code is 204 and contains no data
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)

        # TODO: Once the query endpoint is ready, verify that the pet is actually gone

    @patch("service.routes.InventoryItem.create")
    def test_create_bad_request(self, bad_request_mock):
        """Ensure a 400 is returned if the request data is bad"""
        bad_request_mock.side_effect = DataValidationError()
        test_inventory_item = InventoryItemFactory()
        resp = self.app.post(
            BASE_URL,
            json=test_inventory_item.serialize(),
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_unknown_item(self):
        """Ensure a 404 is returned if a DELETE is sent for a nonexistant item"""
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, "fake_id"),
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed_index(self):
        """Ensure a 405 is returned if a non-GET request is sent to /"""
        resp = self.app.delete(
            "{0}/{1}".format("/", "fake_id"),
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unsupported_media_type(self):
        """Ensure a 415 is raised if an unsupported media type is used"""
        test_inventory_item = InventoryItemFactory()
        resp = self.app.post(
            BASE_URL,
            json=test_inventory_item.serialize(),
            content_type="bad_media_type",
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
