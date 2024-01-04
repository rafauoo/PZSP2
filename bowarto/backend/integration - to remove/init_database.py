# from api.models import *
# from django.utils import timezone

# models = [
#     CompetitionType, FileType, Group, Permission, School,
#     Competition, Application, Participant, File, PermissionGroup, User
# ]
# for model in models[::-1]:
#     model.objects.all().delete()

# for model in models:
#     print(f"{model.__name__: <20} {model.objects.all()}")
# print("Wszytko powyżej jest puste?")
# print('=====================================================')
# CompetitionType.objects.create(name="fotograficzny")
# CompetitionType.objects.create(name="literacki")
# CompetitionType.objects.create(name="artystyczny")

# FileType.objects.create(name="regulamin")
# FileType.objects.create(name="praca konkursowa")

# Group.objects.create(name='admin')
# Group.objects.create(name='editor')
# Group.objects.create(name='user')

# School.objects.create(
#     name='Szkoła Podstawowa nr 1',
#     phone_number='123456789',
#     fax_number='987654321',
#     email='szkola1@example.com',
#     website='http://www.szkola1.pl',
#     city='Warszawa',
#     street='Szkolna',
#     building_number='10',
#     apartment_number='5',
#     postcode='00-001'
# )

# School.objects.create(
#     name='Gimnazjum im. Jana Kochanowskiego',
#     phone_number='234567890',
#     fax_number='876543210',
#     email='gimnazjum@example.com',
#     website='http://www.gimnazjum.pl',
#     city='Kraków',
#     street='Gimnazjalna',
#     building_number='20',
#     apartment_number='3',
#     postcode='30-002'
# )

# School.objects.create(
#     name='Liceum Ogólnokształcące nr 3',
#     phone_number='345678901',
#     fax_number='765432109',
#     email='liceum3@example.com',
#     website='http://www.liceum3.pl',
#     city='Wrocław',
#     street='Licealna',
#     building_number='30',
#     apartment_number='8',
#     postcode='50-003'
# )

# School.objects.create(
#     name='Technikum Informatyczne',
#     phone_number='456789012',
#     fax_number='654321098',
#     email='technikum@example.com',
#     website='http://www.technikum.pl',
#     city='Poznań',
#     street='Techniczna',
#     building_number='40',
#     apartment_number='12',
#     postcode='60-004'
# )

# School.objects.create(
#     name='Szkoła Wyższa XYZ',
#     phone_number='567890123',
#     fax_number='543210987',
#     email='szkola_wyzsza@example.com',
#     website='http://www.szkola-wyzsza.pl',
#     city='Łódź',
#     street='Akademicka',
#     building_number='50',
#     apartment_number='15',
#     postcode='70-005'
# )

# admin_group, created = Group.objects.get_or_create(name='admin')
# editor_group, created = Group.objects.get_or_create(name='editor')
# user_group, created = Group.objects.get_or_create(name='user')

# # Utwórz admina
# admin_user = User.objects.create_user(
#     email='admin@example.com',
#     password='123',
#     first_name='Admin',
#     last_name='User',
#     group=admin_group
# )

# # Utwórz editora
# editor_user = User.objects.create_user(
#     email='editor@example.com',
#     password='123',
#     first_name='Editor',
#     last_name='User',
#     group=editor_group
# )

# for i, school in enumerate(School.objects.all()):
#     User.objects.create_user(
#         email=f'user_{i}@example.com',
#         password='123',
#         first_name='User',
#         last_name=f'{i}',
#         group=user_group
#     )

# competition_type1 = CompetitionType.objects.get(name="fotograficzny")
# competition_type2 = CompetitionType.objects.get(name="literacki")
# competition_type3 = CompetitionType.objects.get(name="artystyczny")

# Competition.objects.create(
#     title='Konkurs Sztuki 2024',
#     description='Międzynarodowy konkurs artystyczny',
#     type=competition_type3,
#     end_at=timezone.now() + timezone.timedelta(days=30)
# )

# Competition.objects.create(
#     title='Konkurs Literacki 2024',
#     description='Konkurs dla utalentowanych pisarzy',
#     type=competition_type2,
#     end_at=timezone.now() + timezone.timedelta(days=45)
# )

# Competition.objects.create(
#     title='Konkurs Naukowy 2024',
#     description='Prezentacja innowacyjnych badań',
#     type=competition_type1,
#     end_at=timezone.now() + timezone.timedelta(days=60)
# )

# Competition.objects.create(
#     title='Konkurs Muzyczny 2024',
#     description='Międzynarodowy festiwal muzyczny',
#     type=competition_type3,
#     end_at=timezone.now() + timezone.timedelta(days=75)
# )

# Competition.objects.create(
#     title='Konkurs Innowacyjnych Projektów 2024',
#     description='Najnowsze pomysły i technologie',
#     type=competition_type1,
#     end_at=timezone.now() + timezone.timedelta(days=90)
# )

# users = User.objects.filter(group__name='user')
# for i, competition in enumerate(Competition.objects.all()):
#     Application.objects.create(
#         competition=competition,
#         user=users[i]
#     )

# for application in Application.objects.all():
#     for i in range(5):
#         Participant.objects.create(
#             email=f'participant_{i + 1}@example.com',
#             application=application,
#             first_name=f'Participant{i + 1}',
#             last_name=f'Lastname{i + 1}'
#         )

# for model in models:
#     print(f"{model.__name__: <20} {model.objects.all()}")
# print("Utworzono bazę testową")
