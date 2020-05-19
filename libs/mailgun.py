import os
from typing import List

import requests
from requests import Response, post

FAILED_LOAD_API_KEY = "Failed to load mailgun API key"
FAILED_LOAD_DOMAIN = "Failed to load mailgun domain"
ERROR_SENDING_EMAIL = "Error to sending confirmation mail. user registration failed."


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    MY_DOMAIN_NAME = os.environ.get('MY_DOMAIN_NAME')
    MY_API_KEY = os.environ.get('MY_API_KEY')
    FROM_TITLE = "Stores REST API"
    FROM_EMAIL = os.environ.get('FROM_EMAIL')

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:

        if cls.MY_API_KEY is None:
            raise MailGunException(FAILED_LOAD_API_KEY)

        if cls.MY_DOMAIN_NAME is None:
            raise MailGunException(FAILED_LOAD_DOMAIN)

        response = requests.post(
            f"https://api.mailgun.net/v3/{cls.MY_DOMAIN_NAME}/messages",
            auth=("api", cls.MY_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": cls.email,
                "subject": "Registration confirmation",
                "text": f"Please click the link to confirm your registration : {link}!"
            }
        )

        if response.status_code != 200:
            raise MailGunException(ERROR_SENDING_EMAIL)