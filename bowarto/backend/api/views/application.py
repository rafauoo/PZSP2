from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Application
from ..serializers.application import ApplicationSerializer


class ApplicationList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['competition']
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().get(request, *args, **kwargs)
            if request.user.is_user:
                user_applications = Application.objects.filter(user=request.user)
                serializer = ApplicationSerializer(user_applications, many=True)
                serialized_data = serializer.data
                return Response(data=serialized_data, status=status.HTTP_200_OK)
            return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.data['user'] = request.user.id
            return super().post(request, *args, **kwargs)
        return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)


class ApplicationDetail(generics.RetrieveDestroyAPIView):
    lookup_field = 'id'
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().get(request, *args, **kwargs)
            if request.user.is_user:
                obj = self.get_object()
                print(obj.user, request.user)
                if obj.user == request.user:
                    return super().get(request, *args, **kwargs)
            return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().delete(request, *args, **kwargs)
            if request.user.is_user:
                obj = self.get_object()
                if obj.user == request.user:
                    return super().delete(request, *args, **kwargs)
            return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)
