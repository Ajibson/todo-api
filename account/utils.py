from rest_framework.views import exception_handler
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from .models import Token


class CustomValidationException(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return self.message

    def to_res(self):
        return self.message

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, CustomValidationException):
        custom_response = exc.to_res()
        return Response(custom_response, status=exc.status_code)

    return response


def pack_response(code: int, data: dict):
    description = 'success' if code == 1 else "error"
    return {"code": code, "description": description, "details": data}

def validate_passwords(password, confirm_password) -> None:
    if len(password) < 8:
        raise CustomValidationException(pack_response(0, {"password": "This password is too short. It must contain at least 8 characters."}), 400)
    if password.isalpha() or password.isnumeric():
        raise CustomValidationException(pack_response(0, {"password": "password must be alphanumeric"}), 400)
    if confirm_password != password:
        raise CustomValidationException(pack_response(0, {"confirm_password": "passwords do not match"}), 400)

def prune_tokens():
    expiration_time = timezone.now() - timedelta(
        days=7
    )  # Assuming a 7-day refresh token lifetime
    Token.objects.filter(blacklisted_at__lte=expiration_time).delete()
