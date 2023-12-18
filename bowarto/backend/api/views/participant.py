from rest_framework import generics

from ..models import Participant
from ..serializers.participant import ParticipantSerializer


class ParticipantList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def get_queryset(self):
        application_id = self.request.query_params.get('application')
        if application_id is None:
            return Participant.objects.all()
        else:
            return Participant.objects.filter(application_id=application_id)


class ParticipantDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer