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

    def test_read_application(self):
        application = Application.objects.create(user=self.user,
                                                 competition=self.competition)
        participant1 = Participant.objects.create(first_name='Participant 1',
                                                  last_name='last',
                                                  email='email@example.com',
                                                  application=application)
        participant2 = Participant.objects.create(first_name='Participant 2',
                                                  last_name='last',
                                                  email='email@example.com',
                                                  application=application)

        serializer = ApplicationSerializer(application)

        expected_data = {
            "id": application.id,
            "user": self.user.id,
            "competition": OrderedDict([
                ("id", self.competition.id),
                ("title", self.competition.title),
                ("description", 'Description for Competition'),
                ("start_at", self.competition.start_at.isoformat()),
                ("end_at", self.competition.end_at.isoformat()),
                ("type", self.competition.get_type_display()),
                ("poster", None),
                ("regulation", None),
            ]),
            "participants": [
                OrderedDict([
                    ("id", participant1.id),
                    ("first_name", participant1.first_name),
                    ("last_name", participant1.last_name),
                    ("email", participant1.email),
                    ("application", application.id),
                ]),
                OrderedDict([
                    ("id", participant2.id),
                    ("first_name", participant2.first_name),
                    ("last_name", participant2.last_name),
                    ("email", participant2.email),
                    ("application", application.id),
                ]),
            ]
        }

        self.assertEqual(serializer.data['id'], expected_data['id'])
        self.assertEqual(serializer.data['user'], expected_data['user'])
        self.assertEqual(serializer.data['competition']['id'],
                         expected_data['competition']['id'])
        # Add similar comparisons for other attributes as needed
        self.assertEqual(serializer.data['participants'][0]['id'],
                         expected_data['participants'][0]['id'])
        self.assertEqual(serializer.data['participants'][1]['id'],
                         expected_data['participants'][1]['id'])
        # Add similar comparisons for participant attributes as needed
