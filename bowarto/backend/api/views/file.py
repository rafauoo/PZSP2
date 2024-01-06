import magic
from rest_framework import generics, status
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
from ..models import File, FileType, User
from ..serializers.file import FileSerializer


class FileList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().get(request, *args, **kwargs)
            if request.user.is_user:
                files = File.objects.filter(participant__application__user=request.user)
                serializer = FileSerializer(files)
                serialised_data = serializer.data
                return Response(serialised_data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = FileSerializer(data=request.data)
            if request.user.is_admin:
                # zapisz plik o dowolnym typie otrzymanym w requescie
                self._post(request, serializer, *args, **kwargs)
            if request.user.is_user:
                file = self.get_object()
                application = file.participant.application
                if application.user == request.user:
                    # zapisz plik o typie "praca konkursowa"
                    file_type = FileType.objects.get(name="praca konkursowa")
                    serializer.data['type'] = file_type
                    self._post(request, serializer, *args, **kwargs)
            return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def _post(self, request, serializer, *args, **kwargs):
        if serializer.is_valid():
            allowed_types = ['application/pdf', 'application/msword',
                             'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
            mime = magic.Magic(mime=True)

            file_content = request.data['path'].read()

            file_type = mime.from_buffer(file_content)

            if file_type not in allowed_types:
                return Response({'error': 'Only PDF and DOCX files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDetail(APIView):
    def get(self, request, id):
        file_instance = get_object_or_404(File, id=id)
        file_content = file_instance.path.read()

        response = HttpResponse(file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'inline; filename="{file_instance.path.name}"'
        return response

    def delete(self, request, id):
        file_instance = get_object_or_404(File, id=id)

        # Usuń plik z storage
        storage_path = file_instance.path.name
        default_storage.delete(storage_path)

        # Usuń obiekt File
        file_instance.delete()

        return Response({'message': 'File deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
