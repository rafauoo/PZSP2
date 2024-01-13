from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from .file import FileSerializer
from ..models import Participant, File
from ..utils import is_allowed_file_type


class ParticipantSerializer(serializers.ModelSerializer):
    attachment = FileSerializer(required=False, allow_null=True)

    class Meta:
        model = Participant
        fields = (
            'id', 'email', 'application', 'first_name', 'last_name',
            'attachment')

    def update(self, instance, validated_data):
        # Update Participant fields
        instance.email = validated_data.get('email', instance.email)
        instance.application = validated_data.get('application',
                                                  instance.application)
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Update or create the File instance
        attachment_data = validated_data.get('attachment', {})
        if not attachment_data or not attachment_data.get('path'):
            instance.attachment.delete()
            instance.attachment = None

        else:
            attachment_serializer = FileSerializer(instance.attachment,
                                                   data=attachment_data,
                                                   allow_null=True,
                                                   required=False)
            if attachment_serializer.is_valid():
                instance.attachment.delete()
                attachment_serializer.save()
                instance.attachment = attachment_serializer.instance

        instance.save()
        return instance
