from rest_framework import serializers

from ..models import PendingApproval


class PendingApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingApproval
        fields = ['id', 'user', 'school']

    def validate(self, data):
        user = data.get('user')
        school = data.get('school')

        if not user or not school:
            raise serializers.ValidationError("User and school are required.")

        return data
