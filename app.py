import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from ma import ma
from resources.user import UserRegister, User, UserLogin, UserActivation, TokenRefresh, AllUser, UserLogout
from resources.item import Item
from blacklist import BLACKLIST


app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')
api = Api(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blacklist_loader
def token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({'description': "Token has been revoked."})


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserActivation, '/activate/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(AllUser, '/users')
api.add_resource(UserLogout, '/logout')
api.add_resource(Item, '/item/<string:name>')


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)