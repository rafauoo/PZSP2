from rest_framework import serializers

from .file import FileSerializer
from ..models import Competition, File
from ..utils import is_allowed_file_type


class CompetitionSerializer(serializers.ModelSerializer):
    poster = FileSerializer(required=False, allow_null=True)
    regulation = FileSerializer(required=False, allow_null=True)

    class Meta:
        model = Competition
        fields = ['id', 'title', 'description', 'start_at', 'end_at', 'type',
                  'poster', 'regulation']

    def create(self, validated_data):
        # Extract nested serializer data
        poster_data = validated_data.pop('poster', {})
        regulation_data = validated_data.pop('regulation', {})

        # Create Competition instance
        competition = Competition.objects.create(**validated_data)

        # Create or update nested serializer instances
        self.create_or_update_nested_serializer(competition, 'poster',
                                                poster_data)
        self.create_or_update_nested_serializer(competition, 'regulation',
                                                regulation_data)

        return competition

    def create_or_update_nested_serializer(self, instance, field_name, data):
        # Helper method to create or update nested serializer instances
        nested_instance = getattr(instance, field_name, None)
        nested_serializer = FileSerializer(nested_instance, data=data,
                                           allow_null=True, required=False)

        if nested_serializer.is_valid():
            if nested_instance:
                nested_instance.delete()
            nested_serializer.save()
            setattr(instance, field_name, nested_serializer.instance)
        instance.save()

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.start_at = validated_data.get('start_at', instance.start_at)
        instance.end_at = validated_data.get('end_at', instance.end_at)

        # TODO zrobić z tego funkcje
        poster_data = validated_data.get('poster', {})
        if not poster_data or not poster_data.get('path'):
            if instance.poster:
                instance.poster.delete()
                instance.poster = None
        else:
            poster_serializer = FileSerializer(instance.poster,
                                               data=poster_data,
                                               allow_null=True,
                                               required=False)
            if poster_serializer.is_valid():
                if instance.poster:
                    instance.poster.delete()
                poster_serializer.save()
                instance.poster = poster_serializer.instance

        # TODO zrobić z tego funkcje
        regulation_data = validated_data.get('regulation', {})
        if not regulation_data or not regulation_data.get('path'):
            if instance.regulation:
                instance.regulation.delete()
                instance.regulation = None
        else:
            regulation_serializer = FileSerializer(instance.regulation,
                                                   data=regulation_data,
                                                   allow_null=True,
                                                   required=False)
            if regulation_serializer.is_valid():
                if instance.regulation:
                    instance.regulation.delete()
                regulation_serializer.save()
                instance.regulation = regulation_serializer.instance
        instance.save()
        return instance
