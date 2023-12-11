from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from ..models import File
from ..serializers.file import FileSerializer


class FileList(ListAPIView):
    lookup_field = 'id'
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = File.objects.all()
    serializer_class = FileSerializer
