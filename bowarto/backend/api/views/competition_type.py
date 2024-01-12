from rest_framework import generics
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import CompetitionType
from ..serializers.competition_type import CompetitionTypeSerializer
from ..permissions import allow_any


@authentication_classes([JWTAuthentication])
class CompetitionTypeList(generics.ListAPIView):
    serializer_class = CompetitionTypeSerializer

    def get_queryset(self):
        return list(CompetitionType)
    
    @allow_any
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
