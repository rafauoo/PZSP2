from rest_framework import generics, status
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from ..models import School
from ..permissions import allow_admin, allow_admin_or_school_user, \
    allow_authenticated, allow_any, allow_admin_or_school_user_or_observer
from ..serializers.school import SchoolSerializer


@authentication_classes([JWTAuthentication])
class SchoolList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @allow_authenticated
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @allow_authenticated
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')

        existing_school = School.objects.filter(email=email).first()
        if existing_school:
            return Response(
                {'message': 'School with this email already exists.'},
                status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


@authentication_classes([JWTAuthentication])
class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @allow_admin_or_school_user_or_observer
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @allow_admin_or_school_user
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @allow_admin_or_school_user
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @allow_admin
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
