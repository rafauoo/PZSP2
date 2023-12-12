from rest_framework import generics

from ..models import School
from ..serializers.school import SchoolSerializer


class SchoolList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
