from collections import OrderedDict
from datetime import datetime

from api.models import Application, Participant, Competition, User
from api.serializers.application import ApplicationSerializer
from django.test import TestCase


class ApplicationSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com',
                                        first_name='John', last_name='Doe',
                                        password='password')
        self.competition = Competition.objects.create(
            title='Test Competition',
            description='Description for Competition',
            start_at=datetime(2024, 1, 1, hour=12, minute=0, second=0,
                              microsecond=0),
            end_at=datetime(2024, 2, 1, hour=12, minute=0, second=0,
                            microsecond=0),
        )

    def test_create_application(self):
        data = {
            "user": self.user.id,
            "competition": self.competition.id,
        }

        serializer = ApplicationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        application = serializer.save()

        self.assertEqual(application.user, self.user)
        self.assertEqual(application.competition, self.competition)

    # def test_read_application(self):
    #     application = Application.objects.create(user=self.user,
    #                                              competition=self.competition)
    #     participant1 = Participant.objects.create(first_name='Participant 1',
    #                                               last_name='last',
    #                                               email='email@example.com',
    #                                               application=application)
    #     participant2 = Participant.objects.create(first_name='Participant 2',
    #                                               last_name='last',
    #                                               email='email@example.com',
    #                                               application=application)
    #
    #     serializer = ApplicationSerializer(application)
    #
    #     expected_data = {
    #         "id": application.id,
    #         "user": self.user.id,
    #         "competition": OrderedDict([
    #             ("id", self.competition.id),
    #             ("title", self.competition.title),
    #             ("description", ""),
    #             ("start_at", self.competition.start_at.isoformat()),
    #             ("end_at", self.competition.end_at.isoformat()),
    #             ("type", "inny"),
    #             ("poster", None),
    #             ("regulation", None),
    #         ]),
    #         "participants": [
    #             OrderedDict([
    #                 ("id", participant1.id),
    #                 ("first_name", participant1.first_name),
    #                 ("last_name", participant1.last_name),
    #                 ("email", participant1.email),
    #                 ("application", application.id),
    #             ]),
    #             OrderedDict([
    #                 ("id", participant2.id),
    #                 ("first_name", participant2.first_name),
    #                 ("last_name", participant2.last_name),
    #                 ("email", participant2.email),
    #                 ("application", application.id),
    #             ]),
    #         ]
    #     }
    #     print(serializer.data)
    #     print(expected_data)
    #     self.assertTrue(are_dicts_equal(serializer.data, expected_data))

# def are_dicts_equal(dict1, dict2):
#     if len(dict1) != len(dict2):
#         return False
#
#     for key, value1 in dict1.items():
#         if key not in dict2:
#             return False
#
#         value2 = dict2[key]
#         if isinstance(value1, dict) and isinstance(value2, dict):
#             if not are_dicts_equal(value1, value2):
#                 return False
#         elif isinstance(value1, list) and isinstance(value2, list):
#             if len(value1) != len(value2):
#                 return False
#             for item1, item2 in zip(value1, value2):
#                 if isinstance(item1, dict) and isinstance(item2, dict):
#                     if not are_dicts_equal(item1, item2):
#                         return False
#                 elif item1 != item2:
#                     return False
#         elif value1 != value2:
#             return False
#
#     return True
