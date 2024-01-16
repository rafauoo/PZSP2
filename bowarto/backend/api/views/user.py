from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import User
from ..permissions import allow_admin, allow_admin_or_this_user, \
    allow_admin_or_observer, allow_admin_or_this_user_or_observer
from ..serializers.user import UserSerializer


@authentication_classes([JWTAuthentication])
class UserList(generics.ListAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @allow_admin_or_observer
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@authentication_classes([JWTAuthentication])
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @allow_admin_or_this_user_or_observer
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @allow_admin
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @allow_admin_or_this_user
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @allow_admin
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
