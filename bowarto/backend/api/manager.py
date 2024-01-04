from django.contrib.auth.models import BaseUserManager

from .models import Group


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        group = Group.objects.get(name="admin")
        extra_fields.setdefault("group", group)
        return self.create_user(email, password, **extra_fields)
