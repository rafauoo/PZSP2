from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from ..models import Permission
from ..serializers.permission import PermissionSerializer


class PermissionList(ListAPIView):
    lookup_field = 'id'
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionDetail(RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer