from rest_framework import serializers

from ..models import Competition, File
from ..utils import is_allowed_file_type


class CompetitionSerializer(serializers.ModelSerializer):
    poster = serializers.PrimaryKeyRelatedField(
        queryset=File.objects.all(),
        required=False,
        allow_null=True
    )
    regulation = serializers.PrimaryKeyRelatedField(
        queryset=File.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Competition
        fields = ['id', 'title', 'description', 'start_at', 'end_at', 'type', 'poster', 'regulation']

    def update(self, instance, validated_data):
        poster_id = validated_data.pop('poster', None)
        regulation_id = validated_data.pop('regulation', None)

        # Perform the regular update on the competition instance
        instance = super().update(instance, validated_data)

        # Handle the update for the nested File fields (poster and regulation)
        if poster_id is not None:
            # Check if the file type is allowed before saving
            poster_content = File.objects.get(id=poster_id).file.read()
            if not is_allowed_file_type(poster_content):
                raise serializers.ValidationError("Invalid file type for poster.")

            instance.poster = File.objects.get(id=poster_id)
            instance.save()

        if regulation_id is not None:
            # Check if the file type is allowed before saving
            regulation_content = File.objects.get(id=regulation_id).file.read()
            if not is_allowed_file_type(regulation_content):
                raise serializers.ValidationError("Invalid file type for regulation.")

            instance.regulation = File.objects.get(id=regulation_id)
            instance.save()

        return instance
