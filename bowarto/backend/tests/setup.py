from api.models import User, UserType
from tests.utils import perform_register


def create_admin(email, password):
    User.objects.create_user(
        email=email,
        password=password,
        first_name='Admin',
        last_name='User',
        user_type=UserType.ADMIN)
    return User.objects.get(email=email)


def create_user(email, password):
    data = {
        'email': email,
        'password': password,
        'first_name': 'Normal',
        'last_name': 'User',
    }
    perform_register(data)
    return User.objects.get(email=email)
