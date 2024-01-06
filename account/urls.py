from django.urls import path

from . import views

# app_name = "account"


urlpatterns = [
    path("register", views.RegisterUser, name="register"),
    path("user", views.GetUser, name="get_user"),
    path("login/token", views.CustomTokenObtainPairView.as_view(), name="token_access"),
    path("login/token/refresh-token", views.CustomTokenRefreshView.as_view(), name="token_refresh"),
]