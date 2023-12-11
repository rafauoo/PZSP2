from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from ..models import Participant
from ..serializers.participant import ParticipantSerializer


class ParticipantList(ListAPIView):
    lookup_field = 'id'
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class ParticipantDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer