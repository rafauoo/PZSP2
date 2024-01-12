from rest_framework import serializers

from .competition import CompetitionSerializer
from .participant import ParticipantSerializer
from ..models import Application, Participant


class ApplicationSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    competition = CompetitionSerializer()

    class Meta:
        model = Application
        fields = ['id', 'competition', 'user', 'participants']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        participants = Participant.objects.filter(application=instance)
        participants_data = ParticipantSerializer(participants, many=True).data
        data['participants'] = participants_data
        return data
