from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from schemas.item import ItemSchema
from models.item import ItemModel

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

ITEM_NOT_FOUND = "The item name {} is not found."
ITEM_ALREADY_EXIST = "Item name {} is already exist."
ITEM_INSERT_SUCCESSFUL = "Item with name {} is inserted successful."
ITEM_UPDATE_SUCCESSFUL = "Item updation successful."
ITEM_DELETE_SUCCESSFUL = "Item name {} has deleted successfully."

class Item(Resource):

    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item)
        return {"Message": ITEM_NOT_FOUND.format(name)}, 401

    @classmethod
    def post(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return {"Message": ITEM_ALREADY_EXIST.format(name)}, 201
        try:
            item_data = item_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 401

        item_data.insert_in_db()
        return {"Message": ITEM_INSERT_SUCCESSFUL.format(name)}, 201

    @classmethod
    def put(cls, name: str):
        item = ItemModel.find_by_name(name)
        if not item:
            return {"Message": ITEM_NOT_FOUND.format(name)}
        try:
            item_data = item_schema.load(request.get_json(), partial=("store_id", "name"))
        except ValidationError as err:
            return err.messages, 401

        item.price = item_data.price
        item.insert_in_db()
        return {"Message": ITEM_UPDATE_SUCCESSFUL}, 201

    @classmethod
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if not item:
            return {"Message": ITEM_NOT_FOUND.format(name)}
        item.delete_from_db()
        return {"Message": ITEM_DELETE_SUCCESSFUL.format(name)}, 201


class ItemList(Resource):

    @classmethod
    def get(cls):
        return {"items": items_schema.dump(ItemModel.find_all())}