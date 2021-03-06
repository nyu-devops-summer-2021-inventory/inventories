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

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

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
            "in_stock": True,
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
        data = {"sku": "FOOBAR12", "count": 5, "condition": "Used", "restock_level": 4}

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

    def test_create(self):
        """Create an inventory item and assert that it exists"""
        inventory_item = InventoryItem(
            sku="FAKESKU123",
            count=10,
            condition="New",
            restock_level=2,
            restock_amount=20,
            in_stock=True,
        )
        self.assertTrue(inventory_item != None)
        self.assertEqual(inventory_item.id, None)
        self.assertEqual(inventory_item.sku, "FAKESKU123")
        self.assertEqual(inventory_item.condition, Condition.New.name)
        self.assertEqual(inventory_item.restock_amount, 20)
        self.assertEqual(inventory_item.in_stock, True)

    def test_delete(self):
        """Ensure InventoryItem.delete() behaves as expected"""
        inventory_item = InventoryItemFactory()
        inventory_item.create()

        # Verify that we have exactly one inventory item first
        self.assertEqual(len(InventoryItem.all()), 1)

        # Then delete the inventory item, and ensure it's no longer in the database
        inventory_item.delete()
        self.assertEqual(len(InventoryItem.all()), 0)

    def test_find_by_sku(self):
        """Ensure find_by_sku returns only items with a given sku"""
        InventoryItem(
            sku="foo",
            count=1,
            condition=Condition.New,
            restock_level=1,
            restock_amount=2,
            in_stock=True,
        ).create()
        InventoryItem(
            sku="bar",
            count=1,
            condition=Condition.OpenBox,
            restock_level=1,
            restock_amount=2,
            in_stock=False,
        ).create()
        items = InventoryItem.find_by_sku("foo")
        self.assertEqual(items[0].sku, "foo")
        self.assertEqual(items[0].count, 1)
        self.assertEqual(items[0].condition, Condition.New)
        self.assertEqual(items[0].restock_level, 1)
        self.assertEqual(items[0].restock_amount, 2)

    def test_find_by_condition(self):
        """Ensure find_by_condition returns only items with a given condition"""
        InventoryItem(
            sku="foo",
            count=1,
            condition=Condition.New,
            restock_level=2,
            restock_amount=3,
            in_stock=True,
        ).create()
        InventoryItem(
            sku="bar",
            count=4,
            condition=Condition.OpenBox,
            restock_level=5,
            restock_amount=6,
            in_stock=False,
        ).create()
        items = InventoryItem.find_by_condition(Condition.OpenBox)
        self.assertEqual(items[0].sku, "bar")
        self.assertEqual(items[0].count, 4)
        self.assertEqual(items[0].condition, Condition.OpenBox)
        self.assertEqual(items[0].restock_level, 5)
        self.assertEqual(items[0].restock_amount, 6)

    def test_find_by_in_stock(self):
        """Ensure find_by_in_stock returns a properly filtered list of inventory items"""
        InventoryItem(
            sku="foo",
            count=1,
            condition=Condition.New,
            restock_level=1,
            restock_amount=2,
            in_stock=True,
        ).create()
        InventoryItem(
            sku="bar",
            count=1,
            condition=Condition.OpenBox,
            restock_level=1,
            restock_amount=2,
            in_stock=False,
        ).create()
        items = InventoryItem.find_by_in_stock(True)
        self.assertEqual(items[0].sku, "foo")
        self.assertEqual(items[0].count, 1)
        self.assertEqual(items[0].condition, Condition.New)
        self.assertEqual(items[0].restock_level, 1)
        self.assertEqual(items[0].restock_amount, 2)
