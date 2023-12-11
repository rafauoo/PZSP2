from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from ..models import School
from ..serializers.school import SchoolSerializer


class SchoolList(ListAPIView):
    lookup_field = 'id'
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
