import os
from flask import Flask
from flask_restful import Api
from db import db
from ma import ma

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)