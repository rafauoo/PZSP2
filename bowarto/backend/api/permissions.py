from rest_framework import status
from rest_framework.response import Response


def allow_any(func):
    def wrapper(self, request, *args, **kwargs):
        return func(self, request, *args, **kwargs)

    return wrapper


def allow_authenticated(func):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(self, request, *args, **kwargs)
        else:
            return Response({'message': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

    return wrapper


def allow_admin(func):
    @allow_authenticated
    def inner_wrapper(self, request, *args, **kwargs):
        if request.user.is_admin:
            return func(self, request, *args, **kwargs)
        else:
            return Response({'message': 'You do not have the necessary permissions'},
                            status=status.HTTP_403_FORBIDDEN)

    return inner_wrapper


def allow_admin_or_school_user(func):
    @allow_authenticated
    def inner_wrapper(self, request, *args, **kwargs):
        school_instance = self.get_object()
        if request.user.is_admin or request.user.school == school_instance:
            return func(self, request, *args, **kwargs)
        else:
            return Response({'message': 'You do not have the necessary permissions'},
                            status=status.HTTP_403_FORBIDDEN)

    return inner_wrapper


def allow_admin_or_this_user(func):
    @allow_authenticated
    def inner_wrapper(self, request, *args, **kwargs):
        user_instance = self.get_object()
        if request.user.is_admin or request.user == user_instance:
            return func(self, request, *args, **kwargs)
        else:
            return Response({'message': 'You do not have the necessary permissions'},
                            status=status.HTTP_403_FORBIDDEN)

    return inner_wrapper


def allow_admin_or_application_creator(func):
    @allow_authenticated
    def wrapper(self, request, *args, **kwargs):
        obj = self.get_object() if hasattr(self, 'get_object') else None
        if request.user.is_admin or (request.user.is_user and obj and obj.user == request.user):
            return func(self, request, *args, **kwargs)
        return Response({'message': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

    return wrapper


def allow_admin_or_participant_creator(func):
    @allow_authenticated
    def wrapper(self, request, *args, **kwargs):
        try:
            participant = self.get_object()
            competition_user = participant.application.user
        except AttributeError:
            return Response({'message': 'Invalid participant or missing attributes'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_admin or competition_user == request.user:
            return func(self, request, *args, **kwargs)

        return Response({'message': 'You do not have the necessary permissions'},
                        status=status.HTTP_403_FORBIDDEN)

    return wrapper
