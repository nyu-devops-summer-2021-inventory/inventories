# TODO: Add a license header
"""
Inventory Service

Paths:
------
GET / - return a homepage of the inventory system
GET /inventories - Returns a list all of the Inventory items
GET /inventories/{id} - Retrieve an inventory item based on id
PUT /inventories/{id} - updates an inventory item record in the database
PUT /inventories/{ID}/in-stock - update the in_stock attribute of Inventory model to True
PUT /inventories/{ID}/out-of-stock - update the in_stock attribute of Inventory model to False
DELETE /inventories/{id} - deletes an inventory item record in the database
"""
from flask import jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound

from service.models import InventoryItem, Condition
from . import status  # HTTP Status Codes

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """
    Return a simple UI for our service
    """
    return app.send_static_file("index.html")


######################################################################
# RETRIEVE AN INVENTORY ITEM
######################################################################
@app.route("/inventories/<int:inventory_item_id>", methods=["GET"])
def get_inventory_items(inventory_item_id):
    """
    Retrieve an inventory item

    This endpoint will return a inventory item based on the id specified in the path
    """
    app.logger.info("Request to Read a inventory item with id [%s]", inventory_item_id)
    inventory_item = InventoryItem.find(inventory_item_id)
    if not inventory_item:
        raise NotFound(
            "Inventory item with id '{}' was not found.".format(inventory_item_id)
        )
    app.logger.info("Found item %s", inventory_item.serialize())
    return make_response(jsonify(inventory_item.serialize()), status.HTTP_200_OK)


######################################################################
# UPDATE AN EXISTING INVENTORY ITEM
######################################################################
@app.route("/inventories/<int:inventory_item_id>", methods=["PUT"])
def update_inventory_items(inventory_item_id):
    """
    Update an inventory item
    This endpoint will update a InventoryItem based the id specified in the path
    """
    app.logger.info(
        "Request to Update a inventory item with id [%s]", inventory_item_id
    )
    check_content_type("application/json")
    inventory_item = InventoryItem.find(inventory_item_id)
    if not inventory_item:
        raise NotFound(
            "Inventory item with id '{}' was not found.".format(inventory_item_id)
        )

    data = request.get_json()
    app.logger.info(data)
    inventory_item.deserialize(data)
    inventory_item.id = inventory_item_id
    inventory_item.update()
    app.logger.info(
        "Inventory item with id [%s] was updated successfully.", inventory_item.id
    )
    return make_response(jsonify(inventory_item.serialize()), status.HTTP_200_OK)


######################################################################
# LIST ALL Inventory Items
######################################################################
@app.route("/inventories", methods=["GET"])
def list_inventories():
    """Returns all of the InventoryItem objects"""
    app.logger.info("Request for inventory list %s", request.args)
    inventory_items = []

    # If a user provides a SKU query parameter, filter by that
    sku = request.args.get("sku")

    # If a user provides a condition parameter, filter by that
    condition = request.args.get("condition")

    # If a user provies an in-stock paramter, filter by that
    in_stock = request.args.get("in_stock")

    if sku:
        inventory_items = InventoryItem.find_by_sku(sku)
    elif condition:
        inventory_items = InventoryItem.find_by_condition(getattr(Condition, condition))
    elif in_stock:
        inventory_items = InventoryItem.find_by_in_stock(in_stock)
    else:
        inventory_items = InventoryItem.all()

    results = [item.serialize() for item in inventory_items]
    app.logger.info("Returning %d inventory items", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# ADD A NEW INVENTORY ITEM
######################################################################
@app.route("/inventories", methods=["POST"])
def create_inventory_item():
    """
    Creates an Inventory item
    This endpoint will create an Inventory item based the data in the body that is posted
    """
    app.logger.info(request.get_json())
    app.logger.info("Request to create an inventory item")
    check_content_type("application/json")
    inventory_item = InventoryItem()
    inventory_item.deserialize(request.get_json())
    inventory_item.create()
    message = inventory_item.serialize()
    location_url = url_for(
        "create_inventory_item", inventory_item_id=inventory_item.id, _external=True
    )

    app.logger.info("Inventory item with ID [%s] created.", inventory_item.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# MARK AN ITEM AS IN-STOCK
######################################################################
@app.route("/inventories/<int:inventory_item_id>/in-stock", methods=["PUT"])
def update_in_stock(inventory_item_id):
    """Update an inventory item to be in-stock based on the provided ID"""
    app.logger.info("Request update inventory item %s to in-stock", inventory_item_id)
    check_content_type("application/json")
    inventory_item = InventoryItem.find(inventory_item_id)
    app.logger.info("Found inventory item %s", inventory_item_id)
    if not inventory_item:
        raise NotFound(inventory_item_id)
    inventory_item.in_stock = True
    inventory_item.update()

    app.logger.info(
        "Inventory item with ID [%s] marked as in-stock.", inventory_item.id
    )
    return make_response(jsonify(inventory_item.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE AN INVENTORY ITEM
######################################################################
@app.route("/inventories/<int:inventory_item_id>", methods=["DELETE"])
def delete_inventory_items(inventory_item_id):
    """
    Delete an inventory item

    This endpoint will delete a InventoryItem based the id specified in the path
    """
    app.logger.info("Request to delete inventory item with id: %s", inventory_item_id)
    inventory_item_id = InventoryItem.find(inventory_item_id)
    if inventory_item_id:
        inventory_item_id.delete()

    app.logger.info("Finished deleting inventory item [%s]", inventory_item_id)
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


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
