from rest_framework import serializers

from .competition import CompetitionSerializer
from .participant import ParticipantSerializer
from ..models import Application, Participant, Competition, User


class ApplicationSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    competition = CompetitionSerializer()

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    competition = serializers.PrimaryKeyRelatedField(
        queryset=Competition.objects.all(), write_only=True)

    class Meta:
        model = Application
        fields = ['id', 'competition', 'user', 'participants']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Dodaj obiekty uczestników i konkursu do odpowiedzi
        participants = Participant.objects.filter(application=instance)
        participants_data = ParticipantSerializer(participants, many=True).data
        data['participants'] = participants_data

        competition_data = CompetitionSerializer(instance.competition).data
        data['competition'] = competition_data

        return data
