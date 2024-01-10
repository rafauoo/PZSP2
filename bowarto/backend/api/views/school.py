from rest_framework import generics
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import School
from ..permissions import allow_admin, allow_admin_or_school_user, allow_authenticated, allow_any
from ..serializers.school import SchoolSerializer


@authentication_classes([JWTAuthentication])
class SchoolList(generics.ListCreateAPIView):
    lookup_field = 'id'
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @allow_any
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @allow_authenticated
    def post(self, request, *args, **kwargs):
        # TODO Przy tworzeniu szkoły sprawdź czy istnieje, jeśli nie to utwórz
        return super().post(request, *args, **kwargs)


# @method_decorator(allow_admin_or_school_user
@authentication_classes([JWTAuthentication])
class SchoolDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @allow_admin_or_school_user
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
