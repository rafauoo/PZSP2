from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models import CompetitionType
from ..serializers.competition_type import CompetitionTypeSerializer


class CompetitionTypeList(generics.ListAPIView):
    lookup_field = 'id'
    queryset = CompetitionType.objects.all()
    serializer_class = CompetitionTypeSerializer
