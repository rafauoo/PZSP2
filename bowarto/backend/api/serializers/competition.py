from rest_framework import serializers

from .competition_type import CompetitionTypeSerializer
from ..models import Competition


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = "__all__"
