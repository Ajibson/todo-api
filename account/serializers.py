from rest_framework import serializers
from .models import Account, Token
from .utils import validate_passwords
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
import datetime
from .utils import pack_response
from rest_framework_simplejwt.exceptions import TokenError


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['username', "password", "confirm_password"]

    def validate(self, data) -> serializers:
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        validate_passwords(password, confirm_password)
        del data["confirm_password"]

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "date_joined",
            "last_login",
        ]

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        representation["date_joined"] = instance.date_joined.strftime(
            "%B %d, %Y, %I:%M %p"
        )
        representation["last_login"] = instance.last_login.strftime(
            "%B %d, %Y, %I:%M %p"
        )
        return representation
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        self.user.last_login = datetime.datetime.now()
        self.user.save()
        # blacklist previous tokens from db and blacklist
        prev_gen_tokens = Token.objects.filter(user=self.user)
        if prev_gen_tokens.exists():
            #  blacklist all token found
            prev_gen_tokens.update(is_blacklisted=True)
        #  TODO: remove tokens from Token table to prevent redundant token laying around: run prune_blacklisted_tokens in utils.py but when
        # add new token to db
        Token.objects.create(
            refresh_token=data["refresh"],
            user=self.user,
        )
        response = pack_response(0, data)
        return response


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        # Call the original validation logic
        data = super().validate(attrs)

        # perform any other validations....
         # Check if the refresh token is blacklisted
        refresh_token_str = self.initial_data.get("refresh", "")
        if Token.objects.filter(refresh_token=refresh_token_str, is_blacklisted=True):
            raise TokenError(pack_response(0, "Invalid token, please log in again"))
        return data