from rest_framework import serializers

from ..models import File
from ..utils import is_allowed_file_type


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'path']

    # def validate_path(self, value):
    #     if not is_allowed_file_type(value.read()):
    #         raise serializers.ValidationError("Invalid file type.")
    #     return value
