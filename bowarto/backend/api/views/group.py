from rest_framework import generics

from ..models import Group
from ..serializers.group import GroupSerializer


class GroupList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
