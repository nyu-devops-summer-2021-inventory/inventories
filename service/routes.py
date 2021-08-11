# TODO: Add a license header
"""
Inventory Service

Paths:
------
GET / - return a homepage of the inventory system
POST /inventories - Creates an Inventory item
GET /inventories - Returns a list all of the Inventory items
GET /inventories/{id} - Retrieve an inventory item based on id
PUT /inventories/{id} - updates an inventory item record in the database
DELETE /inventories/{id} - deletes an inventory item record in the database
PUT /inventories/{ID}/in-stock - update the in_stock attribute of Inventory model to True
"""
from flask import jsonify, request, url_for, make_response, abort
from flask_restx import Api, Resource, fields, reqparse, inputs
from werkzeug.exceptions import NotFound

from service.models import InventoryItem, Condition, DataValidationError
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
# Configure Swagger before initializing it
######################################################################
# Document the type of autorization required

api = Api(
    app,
    version="1.0.0",
    title="Inventory REST API Service",
    description="The inventory service provides an interface for interacting with items in our inventory",  # noqa E503
    default="inventory_items",
    default_label="Inventory item operations",
    doc="/apidocs",  # default also could use doc='/apidocs/'
    authorizations=None,
    prefix="/api",
)


# Define the model so that the docs reflect what can be sent
create_model = api.model(
    "InventoryItem",
    {
        "sku": fields.String(
            required=True, description="The SKU of the inventory item"
        ),
        "count": fields.Integer(
            required=True,
            description="Number of the item that are currently in stock",
        ),
        "condition": fields.String(
            required=True, description="The condition of the item"
        ),
        "restock_level": fields.Integer(
            required=True,
            description="The number of items that will trigger a restock order",
        ),
        "restock_amount": fields.Integer(
            required=True,
            description="The number of items to order when restocking",
        ),
        "in_stock": fields.Boolean(
            required=True, description="The in_stock status of our item"
        ),
    },
)

inventory_item_model = api.inherit(
    "InventoryItemModel",
    create_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)


# query string arguments
inventory_item_args = reqparse.RequestParser()
inventory_item_args.add_argument(
    "sku", type=str, required=False, help="List items by SKU"
)
inventory_item_args.add_argument(
    "count", type=int, required=False, help="List items by count"
)
inventory_item_args.add_argument(
    "condition", type=str, required=False, help="List items by condition"
)
inventory_item_args.add_argument(
    "restock_level", type=int, required=False, help="List items by restock_level"
)
inventory_item_args.add_argument(
    "restock_amount", type=int, required=False, help="List items by restock_amount"
)
inventory_item_args.add_argument(
    "in_stock", type=inputs.boolean, required=False, help="List items by availability"
)

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handles Value Errors from bad data"""
    message = str(error)
    app.logger.error(message)
    return {
        "status_code": status.HTTP_400_BAD_REQUEST,
        "error": "Bad Request",
        "message": message,
    }, status.HTTP_400_BAD_REQUEST


######################################################################
#  PATH: /inventories/{id}
######################################################################
@api.route("/inventories/<inventory_item_id>")
@api.param("inventory_item_id", "The Inventory Item identifier")
class InventoryItemResource(Resource):
    """
    InventoryItemResource class
    Allows the manipulation of a single Inventory Item
    GET /inventories{id} - Returns an inventory item with the id
    PUT /inventories{id} - Update an inventory item with the id
    DELETE /inventories{id} -  Deletes an inventory item with the id
    """

    # ---------------------------------------------------------------------
    # RETRIEVE AN INVENTORY ITEM
    # ---------------------------------------------------------------------
    @api.doc("get_inventory_items")
    @api.response(404, "Inventory item not found")
    @api.marshal_with(inventory_item_model)
    def get(self, inventory_item_id):
        """
        Retrieve an inventory item

        This endpoint will return a inventory item based on the id specified in the path
        """
        app.logger.info(
            "Request to Read a inventory item with id [%s]", inventory_item_id
        )
        inventory_item = InventoryItem.find(inventory_item_id)
        if not inventory_item:
            abort(
                status.HTTP_404_NOT_FOUND,
                "Inventory item with id '{}' was not found.".format(inventory_item_id),
            )
        app.logger.info("Found item %s", inventory_item.serialize())
        return inventory_item.serialize(), status.HTTP_200_OK

    # ---------------------------------------------------------------------
    # UPDATE AN EXISTING INVENTORY ITEM
    # ---------------------------------------------------------------------
    @api.doc("update_inventory_items")
    @api.response(404, "Inventory Item not found")
    @api.response(400, "The posted Inventory Item data was not valid")
    @api.expect(inventory_item_model)
    @api.marshal_with(inventory_item_model)
    def put(self, inventory_item_id):
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

    # ---------------------------------------------------------------------
    # DELETE AN EXISTING INVENTORY ITEM
    # ---------------------------------------------------------------------
    @api.doc("delete_inventory_items")
    @api.response(204, "Inventorty item deleted")
    def delete(self, inventory_item_id):
        """
        Delete an Inventory Item
        This endpoint will delete an Inventory item based the id specified in the path
        """
        app.logger.info(
            "Request to Delete an Inventory item with id [%s]", inventory_item_id
        )
        inventory_item = InventoryItem.find(inventory_item_id)
        if inventory_item:
            inventory_item.delete()
            app.logger.info(
                "Inventory item with id [%s] was deleted", inventory_item_id
            )
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /inventories
######################################################################
@api.route("/inventories", strict_slashes=False)
class InventoryItemCollection(Resource):
    """Handles all interactions with collections of InventoryItem"""

    ######################################################################
    # LIST ALL Inventory Items
    ######################################################################
    @api.doc("list_inventory_items")
    @api.expect(inventory_item_args, validate=True)
    @api.marshal_list_with(inventory_item_model)
    def get(self):
        """Returns all of the InventoryItem objects"""
        app.logger.info(
            "Request for inventory list %s", inventory_item_args.parse_args()
        )
        inventory_items = []
        args = inventory_item_args.parse_args()

        # If a user provides a SKU query parameter, filter by that
        if args["sku"]:
            app.logger.info("Filtering by category: %s", args["sku"])
            inventory_items = InventoryItem.find_by_sku(args["sku"])

        # If a user provides a condition parameter, filter by that
        elif args["condition"]:
            app.logger.info("Filtering by condition: %s", args["condition"])
            try:
                inventory_items = InventoryItem.find_by_condition(
                    getattr(Condition, args["condition"])
                )
            except AttributeError as error:
                raise DataValidationError(
                    f"Invalid condition: {args['condition']}"
                )

        # If a user provies an in-stock paramter, filter by that
        # This is a boolean value, so we need to explictly evaluate it it's not
        # None
        elif args["in_stock"] is not None:
            app.logger.info("Filtering by in stock: %s", args["in_stock"])
            inventory_items = InventoryItem.find_by_in_stock(args["in_stock"])

        else:
            app.logger.info("Returning unfiltered list.")
            inventory_items = InventoryItem.all()

        results = [item.serialize() for item in inventory_items]
        app.logger.info("Returning %d inventory items", len(results))
        return results, status.HTTP_200_OK

    # ---------------------------------------------------------------------
    # ADD A NEW INVENTORY ITEM
    # ---------------------------------------------------------------------
    @api.doc("create_inventory_items")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(inventory_item_model, code=201)
    def post(self):
        """
        Creates an Inventory item
        This endpoint will create an Inventory item based the data in the body that is posted
        """
        app.logger.info("Request to create an inventory item")
        inventory_item = InventoryItem()
        app.logger.info("Payload = %s", api.payload)
        inventory_item.deserialize(api.payload)
        inventory_item.create()
        message = inventory_item.serialize()
        location_url = api.url_for(
            InventoryItemResource, inventory_item_id=inventory_item.id, _external=True
        )
        app.logger.info("Inventory item with ID [%s] created.", inventory_item.id)
        return (
            inventory_item.serialize(),
            status.HTTP_201_CREATED,
            {"Location": location_url},
        )

    # TODO: Refactor the LIST ALL endpoint as a method of this class


######################################################################
# MARK AN ITEM AS IN-STOCK
######################################################################
@api.route("/inventories/<inventory_item_id>/in-stock")
@api.param("inventory_item_id", "The Item identifier")
class InStockResource(Resource):
    """In-stock actions on an item"""

    @api.doc("in-stock")
    @api.response(404, "Item not found")
    def put(self, inventory_item_id):
        """
        Update status of an item to in-stock

        This endpoint will update status of an item to in-stock
        """
        app.logger.info("Update status of an item to in-stock")
        inventory_item = InventoryItem.find(inventory_item_id)
        if not inventory_item:
            abort(
                status.HTTP_404_NOT_FOUND,
                "Item with id [{}] was not found.".format(inventory_item_id),
            )
        inventory_item.in_stock = True
        inventory_item.update()
        app.logger.info("Item with id [%s] is in-stock!!", inventory_item.id)
        return inventory_item.serialize(), status.HTTP_200_OK


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


def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)
