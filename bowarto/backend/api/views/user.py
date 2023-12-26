from rest_framework import generics, status
from rest_framework.response import Response
from ..models import User
from ..serializers.user import UserSerializer


class UserList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().get(request, *args, **kwargs)
            else:
                return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().post(request, *args, **kwargs)
            else:
                return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_instance = self.get_object()
            if hasattr(request.user, 'is_admin') and request.user.is_admin:
                return super().get(request, *args, **kwargs)
            elif request.user == user_instance:
                return super().get(request, *args, **kwargs)
            else:
                return Response({'message': 'You do not have the necessary permissions'},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        user_instance = self.get_object()

        if request.user.is_authenticated:
            if hasattr(request.user, 'is_admin') and request.user.is_admin:
                return super().put(request, *args, **kwargs)
            elif request.user == user_instance:
                return super().put(request, *args, **kwargs)
            else:
                return Response({'message': 'You do not have the necessary permissions'},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        user_instance = self.get_object()

        if request.user.is_authenticated:
            if hasattr(request.user, 'is_admin') and request.user.is_admin:
                return super().delete(request, *args, **kwargs)
            elif request.user == user_instance:
                return super().delete(request, *args, **kwargs)
            else:
                return Response({'message': 'You do not have the necessary permissions'},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
