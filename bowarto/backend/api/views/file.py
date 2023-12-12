from rest_framework import generics

from ..models import File
from ..serializers.file import FileSerializer


class FileList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = File.objects.all()
    serializer_class = FileSerializer
