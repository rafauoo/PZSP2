from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Participant, Application
from ..serializers.participant import ParticipantSerializer


class ParticipantList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['application']
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().get(request, *args, **kwargs)
            if request.user.is_user:
                participants = Participant.objects.filter(application__user=request.user)
                participant_serializer = ParticipantSerializer(participants)
                serialised_data = participant_serializer.data
                return Response(serialised_data, status=status.HTTP_200_OK)
            return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().post(request, *args, **kwargs)
            if request.user.is_user:
                application_id = request.data.get('application')
                try:
                    application = Application.objects.get(id=application_id)
                except Application.DoesNotExist:
                    return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
                if application.user == request.user:
                    return super().post(request, *args, **kwargs)
                return super().post(request, *args, **kwargs)
            return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)


class ParticipantDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().get(request, *args, **kwargs)
            if request.user.is_user:
                participant = self.get_object()
                if participant.competition.user == request.user:
                    return super().get(request, *args, **kwargs)
            return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().put(request, *args, **kwargs)
            if request.user.is_user:
                participant = self.get_object()
                if participant.competition.user == request.user:
                    return super().put(request, *args, **kwargs)
            return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().patch(request, *args, **kwargs)
            if request.user.is_user:
                participant = self.get_object()
                if participant.competition.user == request.user:
                    return super().patch(request, *args, **kwargs)
            return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().delete(request, *args, **kwargs)
            if request.user.is_user:
                participant = self.get_object()
                if participant.competition.user == request.user:
                    return super().delete(request, *args, **kwargs)
            return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)
