from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        dump_only = ("id", "activated")
        load_only = ("password")