import magic
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from functools import wraps

from ..models import File, FileType, User, Participant
from ..permissions import allow_authenticated
from ..serializers.file import FileSerializer


def is_allowed_file_type(file_content):
    allowed_types = ['application/pdf', 'application/msword',
                     'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file_content)
    return file_type in allowed_types


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
            return self.get_files_for_user(request)
        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

    def get_files_for_user(self, request):
        files = File.objects.filter(participant__application__user=request.user)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @allow_authenticated
    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.data)
        if request.user.is_admin:
            return self.create_file_by_admin(request, serializer)
        if request.user.is_user:
            return self.create_file_by_user(request, serializer)
        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

    def create_file_by_user(self, request, serializer):
        participant_id = request.data.get('participant')
        participant = get_object_or_404(Participant, id=participant_id)
        application_user = participant.application.user

        if application_user == request.user:
            file_type = FileType.objects.get(name="praca konkursowa")
            serializer.initial_data['competition'] = None
            serializer.initial_data['type'] = file_type.id
            return self._create_file(request, serializer)

        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

    def create_file_by_admin(self, request, serializer):
        return self._create_file(request, serializer)

    def _create_file(self, request, serializer):
        print(request.data)
        if serializer.is_valid():
            file_content = request.data['path'].read()
            if not is_allowed_file_type(file_content):
                print('not_allowed')
                return Response({'error': 'Only PDF and DOCX files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
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
