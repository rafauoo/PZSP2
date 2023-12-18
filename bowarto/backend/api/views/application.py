from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Application
from ..serializers.application import ApplicationSerializer


class ApplicationList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['competition']

class ApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
