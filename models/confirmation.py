from db import db
from uuid import uuid4
from time import time

CONFIRMATION_EXPIRATION_DELTA = 1800


class ConfirmationModel(db.Model):
    __tablename__ = "confirmations"

    id = db.Column(db.String(80), primary_key=True, nullable=False)
    is_confirmed = db.Column(db.Boolean, nullable=False)
    expire_at = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel")

    def __init__(self, user_id: int, **kwargs):
        self.user_id = user_id
        self.is_confirmed = False
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.id = uuid4().hex

    @classmethod
    def find_by_id(cls, id: str) -> "ConfirmationModel":
        return cls.query.filter_by(id=id).first()

    @property
    def expired(self) -> bool:
        return time() > self.expire_at

    def force_to_expire(self):
        if not self.expired:
            self.expire_at = int(time())
            self.insert_in_db()

    def insert_in_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()