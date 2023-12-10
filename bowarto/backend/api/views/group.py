from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from ..models import Group
from ..serializers.group import GroupSerializer


class GroupList(ListAPIView):
    lookup_field = 'id'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
