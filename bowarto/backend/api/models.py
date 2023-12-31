from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.conf import settings


class Application(models.Model):
    competition = models.ForeignKey('Competition', models.DO_NOTHING)
    user = models.ForeignKey('User', models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'application'

    def __str__(self):
        return f"{self.competition.title} - {self.user}"


class Competition(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey('CompetitionType', models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'competition'

    def __str__(self):
        return self.title


class FileType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'file_type'

    def __str__(self):
        return self.name


class CompetitionType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'competition_type'

    def __str__(self):
        return self.name


class File(models.Model):
    # path = models.FileField(storage=AzureMediaStorage if not settings.TEST else MockAzureMediaStorage())
    path = models.FileField(storage=default_storage)
    type = models.ForeignKey(FileType, models.SET_NULL, blank=True, null=True)
    competition = models.ForeignKey(Competition, models.SET_NULL, blank=True, null=True)
    participant = models.ForeignKey('Participant', models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'file'

    def delete(self, *args, **kwargs):
        # Usuń plik z magazynu przed usunięciem obiektu
        if self.path:
            storage = self.path.storage
            storage.delete(self.path.name)

        # Wywołaj oryginalną funkcję delete
        super().delete(*args, **kwargs)


class Group(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'group'

    def __str__(self):
        return self.name


class Participant(models.Model):
    email = models.EmailField(max_length=255, blank=True, null=True)
    application = models.ForeignKey(Application, models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'participant'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Permission(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'permission'


class PermissionGroup(models.Model):
    group = models.ForeignKey(Group, models.DO_NOTHING)
    permission = models.ForeignKey(Permission, models.DO_NOTHING)

    class Meta:
        unique_together = ('group', 'permission')
        db_table = 'permission_group'


class School(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    fax_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255)
    website = models.URLField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building_number = models.CharField(max_length=10)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    postcode = models.CharField(max_length=10)

    class Meta:
        db_table = 'school'

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    @staticmethod
    def get_default_group():
        default_group, created = Group.objects.get_or_create(name='user')
        return default_group

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School, models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=False, default=get_default_group)

    last_login = None
    USERNAME_FIELD = "email"

    from .manager import CustomUserManager
    objects = CustomUserManager()

    class Meta:
        db_table = 'user'

    @property
    def is_admin(self):
        return self.group.name == 'admin'

    @property
    def is_editor(self):
        return self.group.name == 'editor'

    @property
    def is_user(self):
        return self.group.name == 'user'
