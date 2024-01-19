from rest_framework import serializers

from ..models import File
from ..utils import is_allowed_file_type


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'path']
