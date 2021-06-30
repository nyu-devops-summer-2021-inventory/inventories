# TODO: Add a license header
"""
Inventory Service

Paths:
------
TODO: Add your assigned actions here
PUT /inventories/{ID}/in-stock - update the in_stock attribute of Inventory model to True
PUT /inventories/{ID}/out-of-stock - update the in_stock attribute of Inventory model to False
"""
import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import InventoryItem, DataValidationError

# Import Flask application
from . import app

######################################################################
# UPDATE AN IN_STOCK STATUS
######################################################################
@app.route("/inventories/<int:inventory_item_id>/in-stock", methods=["PUT"])
def update_in_stock(inventory_item_id):
	"""
	Update in-stock status

	This endpoint will update an inventory item's availability based the body that is posted
	"""
	app.logger.info("Request to update in-stock status with id: %s", inventory_item_id)
	check_content_type("application/json")
	inventory_item = InventoryItem.find(inventory_item_id)
	if not inventory_item:
		raise NotFound(inventory_item_id)
	inventory_item.deserialize(request.get_json())
	inventory_item.id = inventory_item_id
	inventory_item.update()

	app.logger.info("Inventory item with ID [%s] updated.", inventory_item.id)
	return make_response(jsonify(inventory_item.serialize()), status.HTTP_200_OK)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
"""
This method is copied straight out of the lab. Please modify if needed.
"""

def check_content_type(media_type):
	"""Checks that the media type is correct"""
	content_type = request.headers.get("Content-Type")
	if content_type and content_type == media_type:
		return
	app.logger.error("Invalid Content-Type: %s", content_type)
	abort(
		status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
		"Content-Type must be {}".format(media_type),
	)