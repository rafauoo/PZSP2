# from typing import Tuple, Optional

# from requests import post

# API_URL = 'http://127.0.0.1:8000/api/'
# LOGIN_URL = API_URL + 'login/'
# REFRESH_URL = API_URL + 'refresh/'
# LOGOUT_URL = API_URL + 'logout/'
# REGISTER_URL = API_URL + 'register/'


# def login(email, password) -> Optional[Tuple[str, str]]:
#     response = post(LOGIN_URL, {'email': email, 'password': password})
#     if response.status_code == 200:
#         response = response.json()
#         refresh_token = response.get('refresh')
#         access_token = response.get('access')
#         if access_token and refresh_token:
#             return access_token, refresh_token
#     return None


# def refresh(refresh_token) -> Optional[str]:
#     response = post(REFRESH_URL, {'refresh': refresh_token})
#     if response.status_code == 200:
#         response = response.json()
#         if response.get('access'):
#             return response.get('access')
#     return None


# def logout(access_token, refresh_token) -> bool:
#     response = post(LOGOUT_URL, json={'access_token': access_token, 'refresh_token': refresh_token})
#     return response.status_code == 200


# def register(user_data: dict) -> Optional[Tuple[str, str]]:
#     response = post(REGISTER_URL, user_data)
#     if response.status_code == 201:
#         response = response.json()
#         refresh_token = response.get('refresh_token')
#         access_token = response.get('access_token')
#         if access_token and refresh_token:
#             return access_token, refresh_token
#     return None
