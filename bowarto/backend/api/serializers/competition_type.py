from rest_framework import serializers
from ..models import CompetitionType


class CompetitionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionType
        fields = ['id', 'name']
