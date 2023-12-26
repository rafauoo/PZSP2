from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .custom_azure import AzureMediaStorage


class Application(models.Model):
    competition = models.ForeignKey('Competition', models.DO_NOTHING)
    user = models.ForeignKey('User', models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'application'


class Competition(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey('CompetitionType', models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'competition'


class FileType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'file_type'


class CompetitionType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'competition_type'


class File(models.Model):
    path = models.FileField(storage=AzureMediaStorage())
    type = models.ForeignKey(FileType, models.SET_NULL, blank=True, null=True)
    competition = models.ForeignKey(Competition, models.SET_NULL, blank=True, null=True)
    participant = models.ForeignKey('Participant', models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'file'


class Group(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'group'


class Participant(models.Model):
    email = models.EmailField(max_length=255, blank=True, null=True)
    application = models.ForeignKey(Application, models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'participant'


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


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School, models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=False)

    last_login = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
