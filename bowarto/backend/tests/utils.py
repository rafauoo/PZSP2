from api.views.auth import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework.test import APIRequestFactory

register_url = '/api/register'
login_url = '/api/login/'
refresh_url = '/api/refresh/'
logout_url = '/api/logout/'


def perform_register(user_data):
    factory = APIRequestFactory()
    request = factory.post(register_url, user_data)
    view = RegisterView.as_view()
    response = view(request)
    return response


def perform_login(login_data):
    factory = APIRequestFactory()
    request = factory.post(login_url, login_data)
    view = TokenObtainPairView.as_view()
    response = view(request)
    return response


def perform_logout(refresh_token):
    factory = APIRequestFactory()
    request_data = {
        'refresh': refresh_token,
    }
    request = factory.post(logout_url, request_data)
    view = TokenBlacklistView.as_view()
    response = view(request)
    return response


def perform_refresh(refresh_token):
    factory = APIRequestFactory()
    request_data = {
        'refresh': refresh_token,
    }
    request = factory.post(refresh_url, request_data)
    view = TokenRefreshView.as_view()
    response = view(request)
    return response
