from rest_framework import serializers

from .file import FileSerializer
from ..models import Participant, File
from ..utils import is_allowed_file_type


class ParticipantSerializer(serializers.ModelSerializer):
    attachment = serializers.PrimaryKeyRelatedField(
        queryset=File.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Participant
        fields = ['id', 'first_name', 'last_name', 'email', 'attachment', 'application']

    def update(self, instance, validated_data):
        attachment_data = validated_data.pop('attachment', None)
        # Perform the regular update on the participant instance
        instance = super().update(instance, validated_data)

        # Handle the update for the nested File field
        if attachment_data:
            # Check if the file type is allowed before saving
            file_content = attachment_data.get('path').read()
            if not is_allowed_file_type(file_content):
                raise serializers.ValidationError("Invalid file type.")

            attachment_serializer = FileSerializer(instance.attachment, data=attachment_data)
            if attachment_serializer.is_valid():
                attachment_serializer.save()

        return instance
