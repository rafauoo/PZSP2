from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CompetitionType(models.TextChoices):
    ARTISTIC = 'artystyczny', _('Artystyczny')
    PHOTOGRAPHIC = 'fotograficzny', _('Fotograficzny')
    LITERARY = 'literacki', _('Literacki')
    OTHER = 'inny', _('Inny')

    @classmethod
    def from_str(cls, value):
        for key in cls:
            if value == key.value.lower():
                return key
        return None


class UserType(models.TextChoices):
    ADMIN = 'admin', _('Admin')
    USER = 'user', _('User')

    @classmethod
    def from_str(cls, value):
        for key in cls:
            if value.lower() == key.value.lower():
                return key
        return None


class File(models.Model):
    path = models.FileField(storage=default_storage)

    class Meta:
        db_table = 'file'

    def delete(self, *args, **kwargs):
        if self.path:
            storage = self.path.storage
            storage.delete(self.path.name)

        super().delete(*args, **kwargs)


class Application(models.Model):
    competition = models.ForeignKey('Competition', models.SET_NULL, null=True)
    user = models.ForeignKey('User', models.SET_NULL, null=True)

    class Meta:
        db_table = 'application'

    def __str__(self):
        return f"{self.competition.title} - {self.user}"


class Competition(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=CompetitionType.choices,
                            default=CompetitionType.OTHER)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    poster = models.OneToOneField(File, on_delete=models.SET_NULL, blank=True,
                                  null=True, unique=True,
                                  related_name='poster_competition')
    regulation = models.OneToOneField(File, on_delete=models.SET_NULL,
                                      blank=True, null=True, unique=True,
                                      related_name='regulation_competition')

    class Meta:
        db_table = 'competition'

    def delete(self, *args, **kwargs):
        if self.poster:
            self.poster.delete()
        if self.regulation:
            self.regulation.delete()
        super().delete()

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.start_at and self.end_at and self.start_at >= self.end_at:
            raise ValidationError(
                "End date must be greater than the start date.")

        valid_competition_types = [tag.value for tag in CompetitionType]
        if self.type and self.type not in valid_competition_types:
            raise ValidationError("Invalid competition type.")

    def save(self, *args, **kwargs):
        self.full_clean()

        # Delete previous attachments before setting new ones
        if self.id:  # Check if it's an existing instance (not a new one)
            original = Competition.objects.get(pk=self.id)
            if original.poster != self.poster:
                original.poster.delete()
            if original.regulation != self.regulation:
                original.regulation.delete()

        super().save(*args, **kwargs)


class Participant(models.Model):
    email = models.EmailField(max_length=255, blank=True, null=True)
    application = models.ForeignKey(Application, models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    attachment = models.OneToOneField(File, on_delete=models.SET_NULL,
                                      blank=True, null=True,
                                      related_name='attachment_participant')

    class Meta:
        db_table = 'participant'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def delete_previous_attachment(self):
        if self.attachment:
            self.attachment.delete()

    def save(self, *args, **kwargs):
        self.full_clean()

        # Delete previous attachment before setting a new one
        if self.id:  # Check if it's an existing instance (not a new one)
            original = Participant.objects.get(pk=self.id)
            if original.attachment != self.attachment:
                original.delete_previous_attachment()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.delete_previous_attachment()
        super().delete(*args, **kwargs)


class School(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    fax_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
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
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School, models.SET_NULL, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=UserType.choices,
                                 default=UserType.USER)

    last_login = None
    USERNAME_FIELD = "email"

    from .manager import CustomUserManager
    objects = CustomUserManager()

    class Meta:
        db_table = 'user'

    @property
    def is_admin(self):
        return self.user_type == UserType.ADMIN.value

    @property
    def is_user(self):
        return self.user_type == UserType.USER.value

    def clean(self):
        super().clean()

        valid_user_types = [tag.value for tag in UserType]
        if self.user_type not in valid_user_types:
            raise ValidationError("Invalid user type.")

        if self.user_type != UserType.USER.value and self.school is not None:
            raise ValidationError(
                "Only users with type 'USER' can have a school.")

    def save(self, *args, **kwargs):
        if self.id:  # Check if the instance is already saved (updating)
            original_user = User.objects.get(id=self.id)
            if self.user_type != original_user.user_type:
                raise ValidationError("Cannot update user_type field.")

        self.full_clean()
        super().save(*args, **kwargs)


class PendingApproval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pending Approval: user: {self.user}, school: {self.school}"

    class Meta:
        db_table = 'pending_approval'
