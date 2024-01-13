from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from .file import FileSerializer
from ..models import Participant, File
from ..utils import is_allowed_file_type


class ParticipantSerializer(serializers.ModelSerializer):
    attachment = FileSerializer(
        required=False)  # Include FileSerializer for the 'attachment' field

    class Meta:
        model = Participant
        fields = (
            'id', 'email', 'application', 'first_name', 'last_name',
            'attachment')

    def create(self, validated_data):
        # Extract 'attachment' data from validated_data if present
        attachment_data = validated_data.pop('attachment', None)

        # Create the participant instance
        participant = Participant.objects.create(**validated_data)

        # If 'attachment' data is present, create the File instance and associate it with the participant
        if attachment_data:
            file_instance = File.objects.create(**attachment_data)
            participant.attachment = file_instance
            participant.save()

        return participant

    def update(self, instance, validated_data):
        # Extract 'attachment' data from validated_data if present
        attachment_data = validated_data.pop('attachment', None)

        # Update the participant instance
        instance.email = validated_data.get('email', instance.email)
        instance.application = validated_data.get('application',
                                                  instance.application)
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if attachment_data:
            if instance.attachment:
                instance.attachment.delete()  # Delete the previous attachment
            file_instance = instance.attachment if instance.attachment else File()
            file_instance.path = attachment_data.get('path', file_instance.path)
            file_instance.save()
            instance.attachment = file_instance

        instance.save()
        return instance
