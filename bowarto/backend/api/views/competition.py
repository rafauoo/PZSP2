from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Competition
from ..serializers.competition import CompetitionSerializer


class CompetitionList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return super().post(request, *args, **kwargs)
            else:
                return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    authentication_classes = [JWTAuthentication]

    def put(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return super().put(request, args, kwargs)
            else:
                return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return super().patch(request, args, kwargs)
            else:
                return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return super().delete(request, args, kwargs)
            else:
                return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Not authorised'}, status=status.HTTP_401_UNAUTHORIZED)
