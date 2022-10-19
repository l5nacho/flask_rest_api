import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)

@app.get("/store")
def get_stores():
    return {"stores": list(stores. values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()

    # Comprobamos que la tienda tenga el campo "Name".
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' are included in the JSON payload.")

    # Comprobamos si la tienda existe
    for store in stores:
        if store_data["name"] == store["name"] and store_data["store_id"] == store["store_id"]:
            abort(400, message="Store already exist.")

    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store

    return new_store, 201

@app.post("/item")
def create_item():
    item_data = request.get_json()

    # Comprobamos si el json de petición tiene todos los valores.
    if ("name" not in item_data
        or "price" not in item_data
        or "store_id" not in item_data):
        abort(400, message="Bad request. Ensure 'name', 'price' and 'store_id' are included in the JSON payload.")

    # Comprobamos si el item existe.
    for item in item.values():
        if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
            abort(400, message="Item already exist.")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id":item_id}
    items[item_id] = item

    return item, 201

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")


@app.get("/store/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")

app.run()

