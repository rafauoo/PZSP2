from rest_framework import serializers
from ..models import CompetitionType


class CompetitionTypeSerializer(serializers.Serializer):
    name = serializers.CharField(source='value')

    class Meta:
        model = CompetitionType

    def to_representation(self, instance):
        return {
            'name': instance.value
        }

    def validate(self, data):
        name = data.get('name')
        competition_type = CompetitionType.from_str(name)
        if competition_type is None:
            raise serializers.ValidationError("Invalid competition type.")
        return data
