from api.models import User, Group
from tests.utils import perform_register


def create_admin(email, password):
    admin_group, _ = Group.objects.get_or_create(name='admin')
    User.objects.create_user(
        email=email,
        password=password,
        first_name='Admin',
        last_name='User',
        group=admin_group
    )
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
