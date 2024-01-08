from rest_framework import generics
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

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

    @allow_admin
    def post(self, request, *args, **kwargs):
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
        return super().put(request, *args, **kwargs)

    @allow_admin
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @allow_admin
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
