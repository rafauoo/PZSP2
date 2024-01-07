from rest_framework import serializers

from ..models import File, FileType, Competition, Participant


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

    def validate(self, data):
        competition = data.get('competition')
        participant = data.get('participant')

        if competition and participant:
            raise serializers.ValidationError("Both competition and participant cannot be set at the same time.")
        elif not competition and not participant:
            raise serializers.ValidationError("Either competition or participant must be set.")
        return data

# class FileUploadSerializer(serializers.Serializer):
#     file = serializers.FileField()
#     type = serializers.PrimaryKeyRelatedField(queryset=FileType.objects.all(), allow_null=True)
#     competition = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all(), allow_null=True)
#     participant = serializers.PrimaryKeyRelatedField(queryset=Participant.objects.all(), allow_null=True)
