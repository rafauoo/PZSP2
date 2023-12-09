# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Application(models.Model):
    competition = models.ForeignKey('Competition', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'application'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Competition(models.Model):
    title = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    type = models.ForeignKey('CompetitionType', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competition'


class CompetitionFileType(models.Model):
    name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competition_file_type'


class CompetitionType(models.Model):
    name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competition_type'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class File(models.Model):
    path = models.CharField(blank=True, null=True)
    type = models.ForeignKey(CompetitionFileType, models.DO_NOTHING, blank=True, null=True)
    competition = models.ForeignKey(Competition, models.DO_NOTHING, blank=True, null=True)
    participant = models.ForeignKey('Participant', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'file'


class Group(models.Model):
    name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group'


class Participant(models.Model):
    email = models.CharField(blank=True, null=True)
    application = models.ForeignKey(Application, models.DO_NOTHING, blank=True, null=True)
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'participant'


class Permission(models.Model):
    name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permission'


class PermissionGroup(models.Model):
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)
    permission = models.ForeignKey(Permission, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permission_group'


class School(models.Model):
    name = models.CharField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True)
    fax_number = models.CharField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    website = models.CharField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    street = models.CharField(blank=True, null=True)
    building_number = models.CharField(blank=True, null=True)
    apartment_number = models.CharField(blank=True, null=True)
    postcode = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'school'


class User(models.Model):
    email = models.CharField(blank=True, null=True)
    password_hash = models.CharField(blank=True, null=True)
    password_salt = models.CharField(blank=True, null=True)
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    school = models.ForeignKey(School, models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
