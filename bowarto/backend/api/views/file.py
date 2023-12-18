from rest_framework import generics
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import File
from ..serializers.file import FileSerializer


class FileList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileDetail(APIView):
    # lookup_field = 'id'
    # queryset = File.objects.all()
    # serializer_class = FileSerializer

# class FileDownloadView(APIView):
    def get(self, request, id):
        file_instance = get_object_or_404(File, id=id)
        file_content = file_instance.path.read()

        response = HttpResponse(file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'inline; filename="{file_instance.path.name}"'
        return response
