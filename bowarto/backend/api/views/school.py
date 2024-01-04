from rest_framework import generics, status
from rest_framework.response import Response

from ..models import School
from ..serializers.school import SchoolSerializer


class SchoolList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get(self, request, *args, **kwargs):
        # return super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().get(request, *args, **kwargs)
            else:
                return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        # return super().post(self, request, *args, **kwargs)
        if request.user.is_authenticated:
            return super().post(self, request, *args, **kwargs)
        else:
            return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)


class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_instance = self.get_object()
            print(user_instance)
            if hasattr(request.user, 'is_admin') and request.user.is_admin:
                return super().get(request, *args, **kwargs)
            elif request.user == user_instance:
                return super().get(request, *args, **kwargs)
        else:
            return Response({'message': 'You do not have the necessary permissions'},
                            status=status.HTTP_403_FORBIDDEN)

    # else:
    #     return Response({'message': 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
