from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from ..models import User
from ..serializers.user import UserSerializer


class UserList(ListAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer