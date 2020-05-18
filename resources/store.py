from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from models.store import StoreModel
from schemas.store import StoreSchema

store_schema = StoreSchema()
stores_schema = StoreSchema(many=True)

STORE_NOT_FOUND = "The store with name {} not found."
STORE_INSERT_SUCCESSFUL_INFO = "The store with name {} inserted successfully."
STORE_ALREADY_EXIST = "The store name {} is already exist."
STORE_UPDATE_SUCCESSFUL = "The store updation successful."
STORE_DELETE_SUCCESSFUL = "The store name {} is deleted successfully."


class Store(Resource):

    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if not store:
            return {"Message": STORE_NOT_FOUND.format(name)}
        return store_schema.dump(store), 201

    @classmethod
    def post(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return {"Message": STORE_ALREADY_EXIST.format(name)}
        try:
            store_data = store_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 401

        store_data.insert_in_db()
        return {"Message": STORE_INSERT_SUCCESSFUL_INFO.format(name)}

    @classmethod
    def put(cls, name: str):
        store = StoreModel.find_by_name(name)
        if not store:
            return {"Message": STORE_NOT_FOUND.format(name)}
        try:
            store_data = store_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 401

        store.name = store_data.name
        store.insert_in_db()
        return {"Message": STORE_UPDATE_SUCCESSFUL}, 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if not store:
            return {"Message": STORE_NOT_FOUND.format(name)}
        store.delete_from_db()
        return {"Messaga": STORE_DELETE_SUCCESSFUL.format(name)}


class StoreList(Resource):

    @classmethod
    def get(cls):
        return {"Stores": stores_schema.dump(StoreModel.find_all())}