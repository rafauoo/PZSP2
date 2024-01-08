from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes

from ..models import Application
from ..permissions import allow_admin_or_application_creator, allow_authenticated
from ..serializers.application import ApplicationSerializer


@authentication_classes([JWTAuthentication])
class ApplicationList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['competition']

    @allow_authenticated
    def get(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().get(request, *args, **kwargs)
        if request.user.is_user:
            return self._get_applications_created_by_user(request.user)
        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

    def _get_applications_created_by_user(self, user):
        user_applications = Application.objects.filter(user=user)
        serializer = ApplicationSerializer(user_applications, many=True)
        serialized_data = serializer.data
        return Response(data=serialized_data, status=status.HTTP_200_OK)

    @allow_authenticated
    def post(self, request, *args, **kwargs):
        if request.user.is_user:
            request.data['user'] = request.user.id
        return super().post(request, *args, **kwargs)


@authentication_classes([JWTAuthentication])
class ApplicationDetail(generics.RetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    @allow_admin_or_application_creator
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @allow_admin_or_application_creator
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
