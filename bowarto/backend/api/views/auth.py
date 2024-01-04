from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ..models import User
from ..serializers.user import UserRegistrationSerializer


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
        data['refresh_token'] = access_token
        data['refresh_token'] = refresh_token

        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh_token")
            access_token = request.data.get("access_token")

            if not refresh_token or not access_token:
                return Response({"detail": "Both access token and refresh token are required."},
                                status=status.HTTP_400_BAD_REQUEST)

            refresh_token_instance = RefreshToken(refresh_token)
            refresh_token_instance.blacklist()
            return Response({"detail": "Tokens successfully invalidated."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
