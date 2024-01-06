from rest_framework import status
from rest_framework.response import Response


def allow_any(func):
    def wrapper(self, request, *args, **kwargs):
        return func(self, request, *args, **kwargs)

    return wrapper


def allow_admin(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return func(self, request, *args, **kwargs)
            else:
                return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

    return wrapper
