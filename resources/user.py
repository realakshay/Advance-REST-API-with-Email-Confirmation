from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

USERNAME_ALREADY_EXIST_INFO = "This username {} is already taken. Please use any other."
USER_REGISTRATION_SUCCESSFUL_INFO = "Congratulations your registration is successful."
USER_NOT_FOUND_ERROR = "The user with user id {} not found."
USER_DELETE_SUCCESSFUL_INFO = "User deleted successful."


class UserRegister(Resource):

    @classmethod
    def post(cls):
        user_json = request.get_json()
        try:
            user_data = user_schema.load(user_json)
        except ValidationError as err:
            return err.messages, 400

        user = UserModel.find_by_username(user_data.username)
        if user:
            return {"Message": USERNAME_ALREADY_EXIST_INFO.format(user_data.username)}, 401

        user_data.insert_in_db()
        return {"Message": USER_REGISTRATION_SUCCESSFUL_INFO}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message": USER_NOT_FOUND_ERROR.format(user_id)}
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message": USER_NOT_FOUND_ERROR.format(user_id)}
        user.delete_from_db()
        return {"Message": USER_DELETE_SUCCESSFUL_INFO}, 201
