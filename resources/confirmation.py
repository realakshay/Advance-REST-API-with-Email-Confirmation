import traceback
from time import time

from flask_restful import Resource

from libs.mailgun import MailGunException
from models.confirmation import ConfirmationModel
from models.user import UserModel
from schemas.confirmation import ConfirmationSchema

confirmation_schema = ConfirmationSchema()

NOT_FOUND_ERROR = "Confirmation reference not found"
LINK_EXPIRED_ERROR = "Confirmation link expired"
ALREADY_CONFIRMED_INFO = "Registration already confirmed."
USER_NOT_FOUND = "User not found"
RESEND_SUCCESSFUL = "Re-Confirmation mail send successful"
RESEND_FAIL = "Re-Confirmation mail send fail"


class Confirmation(Resource):

    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"Message": NOT_FOUND_ERROR}
        if confirmation.expired:
            return {"message": LINK_EXPIRED_ERROR}
        if confirmation.is_confirmed:
            return {"Message": ALREADY_CONFIRMED_INFO}

        confirmation.is_confirmed = True
        confirmation.insert_in_db()
        return {"Message": "success"}


class ConfirmationByUser(Resource):

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message": USER_NOT_FOUND}
        return (
            {
                "current time": int(time()),
                "confirmation": [
                    confirmation_schema.dump(each)
                    for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            },
            200,
        )

    @classmethod
    def post(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message": USER_NOT_FOUND}
        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.is_confirmed:
                    return {"Message": ALREADY_CONFIRMED_INFO}
                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.insert_in_db()
            user.send_confirmation_mail()
            return {"Message": RESEND_SUCCESSFUL}, 201

        except MailGunException as me:
            return {"Message": str(me)}, 501

        except:
            traceback.print_exc()
            return {"Message": RESEND_FAIL}
