from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import User
from ..permissions import allow_authenticated
from ..serializers.user import UserRegistrationSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        refresh = RefreshToken.for_user(serializer.instance)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        data = serializer.data
        data['access'] = access_token
        data['refresh'] = refresh_token

        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


@authentication_classes([JWTAuthentication])
class ProfileView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    @allow_authenticated
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
