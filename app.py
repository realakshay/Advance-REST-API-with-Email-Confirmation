import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from ma import ma
from resources.user import UserRegister, User, UserLogin, UserActivation, TokenRefresh, AllUser


app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')
api = Api(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserActivation, '/activate/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(AllUser, '/users')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)