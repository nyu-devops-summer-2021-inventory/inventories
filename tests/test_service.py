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

	# def test_update_in_stock(self):
	# 	"""Update an existing Pet"""
	# 	# create a pet to update
	# 	test_pet = PetFactory()
	# 	resp = self.app.post(
	# 	BASE_URL, json=test_pet.serialize(), content_type=CONTENT_TYPE_JSON
	# 	)
	# 	self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

	# 	# update the pet
	# 	new_pet = resp.get_json()
	# 	logging.debug(new_pet)
	# 	new_pet["category"] = "unknown"
	# 	resp = self.app.put(
	# 	"/pets/{}".format(new_pet["id"]),
	# 	json=new_pet,
	# 	content_type=CONTENT_TYPE_JSON,
	# 	)
	# 	self.assertEqual(resp.status_code, status.HTTP_200_OK)
	# 	updated_pet = resp.get_json()
	# 	self.assertEqual(updated_pet["category"], "unknown")