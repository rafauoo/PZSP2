from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Participant, Application
from ..permissions import allow_authenticated, allow_admin_or_participant_creator, allow_any, allow_admin
from ..serializers.participant import ParticipantSerializer


@authentication_classes([JWTAuthentication])
class ParticipantList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['application']

    @allow_authenticated
    def get(self, request, *args, **kwargs):
        # return super().get(request, *args, **kwargs)
        if request.user.is_admin:
            return super().get(request, *args, **kwargs)
        if request.user.is_user:
            return self._get_participants_created_by_user(request.user)
        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

    def _get_participants_created_by_user(self, user):
        if self.request.query_params.get('application'):
            user_application = self.request.query_params.get('application')
            user_participants = Participant.objects.filter(application=user_application, application__user=user)
        else:
            user_participants = Participant.objects.filter(application__user=user)
        participant_serializer = ParticipantSerializer(user_participants, many=True)
        serialised_data = participant_serializer.data
        return Response(serialised_data, status=status.HTTP_200_OK)

    @allow_authenticated
    def post(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().post(request, *args, **kwargs)
        if request.user.is_user:
            return self._create_participant(request, *args, **kwargs)
        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

    def _create_participant(self, request, *args, **kwargs):
        application_id = request.data.get('application')
        attachment_file = request.data.get('attachment')  # Assuming 'attachment' is the key for the file field

        try:
            application = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

        if application.user == request.user:
            # Create a dictionary with your data including the file
            participant_data = {
                'email': request.data.get('email'),
                'application': application_id,
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'attachment': attachment_file,
            }
            participant_serializer = ParticipantSerializer(data=participant_data)

            if participant_serializer.is_valid():
                participant_serializer.save()
                return Response(participant_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(participant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)


@authentication_classes([JWTAuthentication])
class ParticipantDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    @allow_admin_or_participant_creator
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @allow_admin_or_participant_creator
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @allow_admin_or_participant_creator
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @allow_admin_or_participant_creator
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
