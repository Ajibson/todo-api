from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers  import RegistrationSerializer, UserSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from django.db import transaction
from .utils import pack_response
from rest_framework import status
import logging
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



logger = logging.getLogger(__name__)



# Create your views here.
@api_view(["POST"])
def RegisterUser(request) -> Response:
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # start a new transaction: this ensure that both account and and any other important actions got created.
    with transaction.atomic():
        try:
            instance = serializer.save()
            instance.set_password(serializer.validated_data.get("password"))
            instance.save()
            return Response(
            pack_response(1, {"username": serializer.validated_data["username"]}),
            status.HTTP_201_CREATED,
            )
        except Exception as e:  # pragma: no cover
            transaction.set_rollback(True)
            logger.error(f"Account creation failed: {e}", exc_info=1)
            return Response(
                pack_response(0, f"Account creation failed: {e}"),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["GET"])
# @permission_classes([IsAuthenticatedAndNotBlacklisted])
def GetUser(requests):
    user = requests.user
    serializer = UserSerializer(user)
    return Response(pack_response(1, serializer.data))



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer