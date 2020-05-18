from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    items = db.relationship('ItemModel', lazy="dynamic")

    @classmethod
    def find_by_name(cls, name: str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()
