import copy

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, parser_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser

from ..models import Competition
from ..permissions import allow_any, allow_admin
from ..serializers.competition import CompetitionSerializer


@authentication_classes([JWTAuthentication])
class CompetitionList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

    @allow_any
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @allow_any
    def post(self, request, *args, **kwargs):
        keys_to_remove = [key for key in request.data if
                          key in ('regulation.path', 'poster.path') and not
                          request.data[key]]
        if keys_to_remove:
            data_copy = copy.copy(request.data)
            for key in keys_to_remove:
                del data_copy[key]
            serializer = CompetitionSerializer(data=data_copy)
            serializer.is_valid(raise_exception=True)
            instance = serializer.create(serializer.validated_data)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return super().post(request, *args, **kwargs)


@authentication_classes([JWTAuthentication])
class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

    @allow_any
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @allow_admin
    def put(self, request, *args, **kwargs):
        keys_to_remove = [key for key in request.data if
                          key in ('regulation.path', 'poster.path') and not
                          request.data[key]]
        if keys_to_remove:
            data_copy = copy.copy(request.data)
            for key in keys_to_remove:
                del data_copy[key]
            serializer = CompetitionSerializer(data=data_copy)
            serializer.is_valid(raise_exception=True)
            instance = self.get_object()
            instance = serializer.update(instance, serializer.validated_data)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().put(request, *args, **kwargs)

    @allow_admin
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @allow_admin
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
