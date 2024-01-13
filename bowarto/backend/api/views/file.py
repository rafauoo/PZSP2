from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.utils.http import content_disposition_header
from ..models import File, Participant
from ..permissions import allow_authenticated, allow_any
from ..serializers.file import FileSerializer


@authentication_classes([JWTAuthentication])
class FileList(generics.ListAPIView):
    lookup_field = 'id'
    queryset = File.objects.all()
    serializer_class = FileSerializer

    @allow_authenticated
    def get(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().get(request, *args, **kwargs)
        if request.user.is_user:
            return self.get_files_for_user(request)
        return Response({'message': 'Not permitted'},
                        status=status.HTTP_403_FORBIDDEN)

    def get_files_for_user(self, request):
        files = File.objects.filter(
            attachment_participant__application__user=request.user)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
class FileDetail(generics.RetrieveDestroyAPIView):
    queryset = File.objects.all()
    lookup_field = 'id'

    @allow_any
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        return self._get_file_by_id(id)

    def _get_file_by_id(self, id):
        file_instance = get_object_or_404(File, id=id)
        file_content = file_instance.path.read()
        response = HttpResponse(file_content,
                                content_type='application/octet-stream')
        response['Content-Disposition'] = content_disposition_header(False,
                                                                     file_instance.path.name)
        return response

    # @allow_authenticated
    def delete(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        if request.user.is_admin or self._is_user_permitted(request.user, id):
            return self._delete_file_by_id(id)
        return Response({'message': 'Not permitted'},
                        status=status.HTTP_403_FORBIDDEN)

    def _is_user_permitted(self, user, file_id):
        try:
            file_instance = File.objects.get(id=file_id)
            participant = file_instance.attachment_participant
            return user.is_user and participant.application.user == user
        except (File.DoesNotExist, Participant.DoesNotExist):
            return False

    def _delete_file_by_id(self, id):
        file_instance = get_object_or_404(File, id=id)

        storage_path = file_instance.path.name
        default_storage.delete(storage_path)

        file_instance.delete()
        return Response({'message': 'File deleted successfully.'},
                        status=status.HTTP_204_NO_CONTENT)
