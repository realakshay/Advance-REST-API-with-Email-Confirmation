from flask import Flask
from db import db
from ma import ma

app = Flask(__name__)

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)