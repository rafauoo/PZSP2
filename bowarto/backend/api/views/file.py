import magic
from rest_framework import generics, status
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import File, FileType, User
from ..permissions import allow_authenticated
from ..serializers.file import FileSerializer


@authentication_classes([JWTAuthentication])
class FileList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = File.objects.all()
    serializer_class = FileSerializer

    @allow_authenticated
    def get(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().get(request, *args, **kwargs)
        if request.user.is_user:
            return self._get_files_created_by_user(request)
        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

    def _get_files_created_by_user(self, request):
        files = File.objects.filter(participant__application__user=request.user)
        serializer = FileSerializer(files, many=True)
        serialised_data = serializer.data
        return Response(serialised_data, status=status.HTTP_200_OK)

    @allow_authenticated
    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        if request.user.is_admin:
            self._post_file_by_admin(request, serializer)
        if request.user.is_user:
            self._post_file_by_user(request, serializer)
        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

    def _post_file_by_user(self, request, serializer):
        file = self.get_object()
        application = file.participant.application
        if application.user == request.user:
            file_type = FileType.objects.get(name="praca konkursowa")
            serializer.data['type'] = file_type
            self._post(request, serializer)

    def _post_file_by_admin(self, request, serializer):
        self._post(request, serializer)

    def _file_type_is_allowed(self, file_content):
        allowed_types = ['application/pdf', 'application/msword',
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file_content)

        if file_type not in allowed_types:
            return Response({'error': 'Only PDF and DOCX files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

    def _post(self, request, serializer):
        if serializer.is_valid():
            file_content = request.data['path'].read()
            self._file_type_is_allowed(file_content)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDetail(generics.RetrieveDestroyAPIView):
    @allow_authenticated
    def get(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        if request.user.is_admin:
            return self._get_file_by_id(id)
        if request.user.is_user:
            file = self.get_object()
            if file.participant.application.user == request.user:
                return self._get_file_by_id(id)
        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

    def _get_file_by_id(self, id):
        file_instance = get_object_or_404(File, id=id)
        file_content = file_instance.path.read()

        response = HttpResponse(file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'inline; filename="{file_instance.path.name}"'
        return response

    @allow_authenticated
    def delete(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        if request.user.is_admin:
            return self._delete_file_by_id(id)
        if request.user.is_user:
            file = self.get_object()
            if file.participant.application.user == request.user:
                return self._delete_file_by_id(id)
        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

    def _delete_file_by_id(self, id):
        file_instance = get_object_or_404(File, id=id)

        storage_path = file_instance.path.name
        default_storage.delete(storage_path)

        file_instance.delete()
        return Response({'message': 'File deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
