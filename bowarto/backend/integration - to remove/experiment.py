# import json

# from auth import login, refresh
# from requests import get, post, delete

# API_URL = 'http://127.0.0.1:8000/api/'


# def refresh_token():
#     try:
#         access_token, refresh_token = login("admin@example.com", '123')
#         print(refresh_token)
#     except TypeError as e:
#         print(e)


# def admin_create_competition():
#     access_token, refresh_token = login("admin@example.com", '123')

#     types = get(API_URL + 'competition_types/').json()

#     literary_competition_id = next(
#         (comp_type['id'] for comp_type in types if comp_type['name'] == 'literacki'), None)

#     new_competition = {
#         "title": "Test Competition",
#         "description": "test description",
#         "end_at": "2024-11-11T00:00:00Z",
#         "type": literary_competition_id
#     }

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     response = post(API_URL + 'competitions/', data=json.dumps(new_competition), headers=headers)

#     assert response.status_code == 201


# def user_create_competition():
#     access_token, refresh_token = login("user_0@example.com", '123')

#     types = get(API_URL + 'competition_types/').json()

#     literary_competition_id = next(
#         (comp_type['id'] for comp_type in types if comp_type['name'] == 'literacki'), None)

#     new_competition = {
#         "title": "Test Competition",
#         "description": "test description",
#         "end_at": "2024-11-11T00:00:00Z",
#         "type": literary_competition_id
#     }

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     response = post(API_URL + 'competitions/', data=json.dumps(new_competition), headers=headers)

#     assert response.status_code == 403


# def user_create_application():
#     access_token, refresh_token = login("user_0@example.com", '123')

#     competitions = get(API_URL + 'competitions/').json()

#     competition_id = competitions[0]['id']

#     new_application = {
#         'competition': competition_id
#     }

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     response = post(API_URL + 'applications/', data=json.dumps(new_application), headers=headers)
#     print(response.json())


# def user_get_applications():
#     access_token, refresh_token = login("user_0@example.com", '123')
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }
#     response = get(API_URL + 'applications/', headers=headers)
#     print(response.json())


# def user_one_application():
#     access_token, refresh_token = login("user_0@example.com", '123')
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     response = get(API_URL + 'applications/', headers=headers).json()
#     application_id = response[0]['id']

#     response = get(API_URL + f'applications/{application_id}/', headers=headers)
#     print(response.json())

#     response = delete(API_URL + f'applications/{application_id}/', headers=headers)

#     assert response.status_code == 204


# def user_one_application_created_by_another_user():
#     access_token, refresh_token = login("user_0@example.com", '123')
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     response = get(API_URL + 'applications/', headers=headers).json()
#     application_id = response[0]['id']

#     # login to another user
#     access_token, refresh_token = login("user_1@example.com", '123')
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     response = get(API_URL + f'applications/{application_id}/', headers=headers)
#     print(response.json())
#     assert response.status_code == 403

#     response = delete(API_URL + f'applications/{application_id}/', headers=headers)
#     assert response.status_code == 403


# if __name__ == '__main__':
#     # test_admin_create_competition()
#     # test_user_create_competition()
#     user_create_application()
#     # test_user_get_applications()
#     # test_user_one_application()
#     user_one_application_created_by_another_user()
