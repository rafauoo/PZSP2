from rest_framework import serializers

from ..models import File, CompetitionFileType, Competition, Participant


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"



class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    type = serializers.PrimaryKeyRelatedField(queryset=CompetitionFileType.objects.all(), allow_null=True)
    competition = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all(), allow_null=True)
    participant = serializers.PrimaryKeyRelatedField(queryset=Participant.objects.all(), allow_null=True)



