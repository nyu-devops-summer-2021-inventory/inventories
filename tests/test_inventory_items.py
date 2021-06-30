# TODO: Copyright header

"""
Test cases for InventoryItem Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_inventory_items.py:TestInventoryItemModel

"""
import os
import logging
import unittest

from service.models import InventoryItem, Condition, DataValidationError, db

from service import app
from .factories import InventoryItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  I N V E N T O R Y   M O D E L   T E S T   C A S E S
######################################################################
class TestInventoryItemModel(unittest.TestCase):
    """Test Cases for InventoryItem Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        InventoryItem.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    def test_serialize(self):
        """Test serialization of an InventoryItem"""
        item = InventoryItemFactory()

        # Serialize will return our data in a dictionary
        data = item.serialize()

        # Make sure we actually got data back from the call to serialize()
        self.assertIsNotNone(data)

        # I.e. make sure we have an ID key in our dict and that it's the same
        # as the ID attribute in the item we generated
        self.assertIn("id", data)
        self.assertEqual(data["id"], item.id)

        # Same as above, but for SKU
        self.assertIn("sku", data)
        self.assertEqual(data["sku"], item.sku)

        # Same as above, but for count
        self.assertIn("count", data)
        self.assertEqual(data["count"], item.count)

        # Same as above, but for condition
        self.assertIn("condition", data)
        self.assertEqual(data["condition"], item.condition.name)

        # Same as above, but for restock_level
        self.assertIn("restock_level", data)
        self.assertEqual(data["restock_level"], item.restock_level)

        # Same as above, but for restock_amount
        self.assertIn("restock_amount", data)
        self.assertEqual(data["restock_amount"], item.restock_amount)

        # Same as above, but for in_stock
        self.assertIn("in_stock", data)
        self.assertEqual(data["in_stock"], item.in_stock)

    def test_deserialize(self):
        """Test deserialization of an InventoryItem"""
        data = {
            "sku": "FAKE1234",
            "count": 10,
            "condition": "New",
            "restock_level": 2,
            "restock_amount": 20,
            "in_stock": True
        }

        # Create a blank slate InventoryItem
        item = InventoryItem()

        item.deserialize(data)

        # Ensure we actually got data in our input
        self.assertIsNotNone(item)

        # We didn't commit this to the database yet, so a primary key has not
        # yet been assigned
        self.assertEqual(item.id, None)

        # Assert our SKU is correct
        self.assertEqual(item.sku, "FAKE1234")

        # Assert our count is correct
        self.assertEqual(item.count, 10)

        # Assert our condition is correct
        self.assertEqual(item.condition, Condition.New)

        # Assert our restock level is correct
        self.assertEqual(item.restock_level, 2)

        # Assert our restock amount is correct
        self.assertEqual(item.restock_amount, 20)

    def test_deserialize_missing_data(self):
        """Test deserialization of an InventoryItem with missing data"""
        # I.e. we're missing a restock_amount
        data = {
            "sku": "FOOBAR12", 
            "count": 5, 
            "condition": "Used", 
            "restock_level": 4
        }

        # Construct an empty InventoryItem
        item = InventoryItem()

        # Use assertRaises as a context manager:
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises  # noqa E503
        with self.assertRaises(DataValidationError):
            item.deserialize(data)

    def test_deserialize_bad_data(self):
        """Test deserialization of an InventoryItem with bad data"""
        data = "I am going to break your Database!!!"
        item = InventoryItem()

        with self.assertRaises(DataValidationError):
            item.deserialize(data)

    def test_repr(self):
        """Ensure string representation of an InventoryItem is correct"""
        item = InventoryItem()
        # Use deserialize so we have control over all of the attributes for 
        # our assertEqual statement
        item.deserialize(
            {
                "sku": "FAKE1234",
                "count": 10,
                "condition": "New",
                "restock_level": 2,
                "restock_amount": 20,
                "in_stock": True,
            }   
        )
        expected = "<Inventory item FAKE1234 id=None>"
        self.assertEqual(item.__repr__(), expected)