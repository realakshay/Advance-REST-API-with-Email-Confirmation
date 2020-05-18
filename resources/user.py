from flask import request
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_raw_jwt
from marshmallow import ValidationError

from blacklist import BLACKLIST
from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

USERNAME_ALREADY_EXIST_INFO = "This username {} is already taken. Please use any other."
USER_REGISTRATION_SUCCESSFUL_INFO = "Congratulations your registration is successful."
USER_NOT_FOUND_ERROR = "The user with user id {} not found."
USER_DELETE_SUCCESSFUL_INFO = "User deleted successful."
USER_NOT_ACTIVATED_ERROR = "The user with id {} is not activated yet."
INVALID_CREDENTIALS_INFO = "Provided info not valid. Please check your credentials."
USER_ALREADY_ACTIVATED = "The user with id {} is already activated."
USER_ACTIVATION_SUCCESSFUL_INFO = "The user is activated successful with user id {}."
USER_LOGOUT_SUCCESSFUL_INFO = "The user have successfully logged out."


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


class UserLogin(Resource):

    @classmethod
    def post(cls):
        user_json = request.get_json()
        try:
            user_data = user_schema.load(user_json)
        except ValidationError as err:
            return err.messages, 401

        user = UserModel.find_by_username(user_data.username)
        if user and safe_str_cmp(user_data.password, user.password):
            if user.activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 201
            return {"Message": USER_NOT_ACTIVATED_ERROR.format(user.id)}, 401
        return {"Message": INVALID_CREDENTIALS_INFO}, 401


class UserActivation(Resource):

    @classmethod
    def get(cls, user_id: int):

        user = UserModel.find_by_id(user_id)
        if user:
            if user.activated:
                return {"Message": USER_ALREADY_ACTIVATED.format(user_id)}
            user.activated = True
            user.insert_in_db()
            return {"Message": USER_ACTIVATION_SUCCESSFUL_INFO.format(user_id)}
        return {"Message": USER_NOT_FOUND_ERROR.format(user_id)}


class TokenRefresh(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        user_id = get_jwt_identity()
        fresh_token = create_access_token(identity=user_id, fresh=False)
        return {"fresh_token": fresh_token}


class UserLogout(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"Message": USER_LOGOUT_SUCCESSFUL_INFO}, 201


class AllUser(Resource):

    @classmethod
    def get(cls):
        return {"Users": users_schema.dump(UserModel.find_all())}
