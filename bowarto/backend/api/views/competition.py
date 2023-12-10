from rest_framework import generics

from ..models import Competition
from ..serializers.competition import CompetitionSerializer


class CompetitionList(generics.ListAPIView):
    lookup_field = 'id'
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
