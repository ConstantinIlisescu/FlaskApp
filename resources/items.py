import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from db import stores


blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get_all_items():
        return{"items":list(items.values())}
            

    def create_item():
        item_data = request.get_json()
        # Here not only we need to validate data exists,
        # but also what type of data. Price should be a float, etc.
        if(
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data
        ):
            abort(
                400,
                message="Bad request. ensure 'price', 'store_id', and 'name' are included in the JSON payload"
            )
        for item in items.values():
            if(
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists.")
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found.")
        
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        
        return item, 201
    
    
    
    
@blp.route("/item")
class ItemList(MethodView):
    def get(item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")


    def delete(item_id):
        try:
            del items[item_id]
            return {"message":"Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")


    def put(item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.")

        try:
            item = items[item_id]
            item |= item_data  # syntax to update an dictionary, the items from the item_data will replace the values from item or add them to item
            
            return item
        except KeyError:
            abort(404, message="Item not found")