from rest_framework import generics

from ..models import Permission
from ..serializers.permission import PermissionSerializer


class PermissionList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionDetail(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer