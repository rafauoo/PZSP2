from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CompetitionType(models.TextChoices):
    """
    Enumeration representing different types of competitions.

    Choices:
    - ARTISTIC: Artystyczny
    - PHOTOGRAPHIC: Fotograficzny
    - LITERARY: Literacki
    - OTHER: Inny
    """

    ARTISTIC = 'artystyczny', _('Artystyczny')
    PHOTOGRAPHIC = 'fotograficzny', _('Fotograficzny')
    LITERARY = 'literacki', _('Literacki')
    OTHER = 'inny', _('Inny')

    @classmethod
    def from_str(cls, value):
        """
        Convert a lowercase string to the corresponding CompetitionType.

        Parameters:
        - value (str): A lowercase string representing a competition type.

        Returns:
        - CompetitionType or None: The corresponding CompetitionType if found,
          or None if the value doesn't match any competition type.
        """
        for key in cls:
            if value == key.value.lower():
                return key
        return None


class UserType(models.TextChoices):
    """
    Enumeration representing different types of user roles.

    Choices:
    - ADMIN: Admin
    - USER: User
    - OBSERVER: Observer
    """

    ADMIN = 'admin', _('Admin')
    USER = 'user', _('User')
    OBSERVER = 'observer', _('Observer')

    @classmethod
    def from_str(cls, value):
        """
        Convert a case-insensitive string to the corresponding UserType.

        Parameters:
        - value (str): A case-insensitive string representing a user type.

        Returns:
        - UserType or None: The corresponding UserType if found,
          or None if the value doesn't match any user type.
        """
        for key in cls:
            if value.lower() == key.value.lower():
                return key
        return None


class File(models.Model):
    """
    Model representing a file with its storage path.

    Fields:
    - path (FileField): The file path stored using the default storage.

    Meta:
    - db_table (str): Database table name for the File model.
    """

    path = models.FileField(storage=default_storage)

    class Meta:
        db_table = 'file'

    def delete(self, *args, **kwargs):
        """
        Override the delete method to delete the associated file from storage.

        This method deletes the file associated with the model instance from the
        storage system before deleting the model instance itself.

        Parameters:
        - args: Positional arguments passed to the superclass delete method.
        - kwargs: Keyword arguments passed to the superclass delete method.
        """
        if self.path:
            storage = self.path.storage
            storage.delete(self.path.name)

        super().delete(*args, **kwargs)


class Application(models.Model):
    """
    Model representing a user's application to a competition.

    Fields:
    - competition (ForeignKey): Reference to the Competition the application is for.
    - user (ForeignKey): Reference to the User who submitted the application.

    Meta:
    - db_table (str): Database table name for the Application model.
    """

    competition = models.ForeignKey('Competition', models.CASCADE, null=True)
    user = models.ForeignKey('User', models.SET_NULL, null=True)

    class Meta:
        db_table = 'application'

    def __str__(self):
        """
        Return a string representation of the application.

        Returns:
        - str: A string containing the competition title and the user's username.
        """
        return f"{self.competition.title} - {self.user}"


class Competition(models.Model):
    """
    Model representing a competition.

    Fields:
    - title (CharField): Title of the competition.
    - description (TextField): Description of the competition.
    - type (CharField): Type of the competition (e.g., ARTISTIC, PHOTOGRAPHIC).
    - start_at (DateTimeField): Start date and time of the competition.
    - end_at (DateTimeField): End date and time of the competition.
    - poster (OneToOneField): Reference to a File instance representing the competition's poster.
    - regulation (OneToOneField): Reference to a File instance representing the competition's regulation.

    Meta:
    - db_table (str): Database table name for the Competition model.
    """

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
        """
        Override the delete method to delete associated poster and regulation files.

        This method deletes the associated poster and regulation files from the storage system
        before deleting the competition model instance itself.

        Parameters:
        - args: Positional arguments passed to the superclass delete method.
        - kwargs: Keyword arguments passed to the superclass delete method.
        """
        if self.poster:
            self.poster.delete()
        if self.regulation:
            self.regulation.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the competition.

        Returns:
        - str: The title of the competition.
        """
        return self.title

    def clean(self):
        """
        Validate the competition data.

        Raises:
        - ValidationError: If the start date is greater than or equal to the end date,
          or if the competition type is invalid.
        """
        super().clean()
        if self.start_at and self.end_at and self.start_at >= self.end_at:
            raise ValidationError(
                "End date must be greater than the start date.")

        valid_competition_types = [tag.value for tag in CompetitionType]
        if self.type and self.type not in valid_competition_types:
            raise ValidationError("Invalid competition type.")


class Participant(models.Model):
    """
    Represents a participant in the application system.

    Attributes:
        email (models.EmailField): The email address of the participant.
        application (models.ForeignKey): A foreign key relationship to the associated Application.
        first_name (models.CharField): The first name of the participant.
        last_name (models.CharField): The last name of the participant.
        attachment (models.OneToOneField): A one-to-one relationship with a File, representing an attachment.
    """
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
        """
        Returns a string representation of the participant.

        Returns:
            str: A formatted string with the first and last name of the participant.
        """
        return f'{self.first_name} {self.last_name}'

    def delete_previous_attachment(self):
        """
        Deletes the previous attachment associated with the participant, if it exists.
        """
        if self.attachment:
            self.attachment.delete()

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to perform additional actions before saving.

        This method ensures that the previous attachment is deleted before setting a new one if it has changed.
        """
        self.full_clean()

        # Delete previous attachment before setting a new one
        if self.id:  # Check if it's an existing instance (not a new one)
            original = Participant.objects.get(pk=self.id)
            if original.attachment != self.attachment:
                original.delete_previous_attachment()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Overrides the default delete method to ensure that the previous attachment is deleted before deleting the participant.
        """
        self.delete_previous_attachment()
        super().delete(*args, **kwargs)


class School(models.Model):
    """
    Represents a school in the education system.

    Attributes:
        name (models.CharField): The name of the school.
        phone_number (models.CharField): The phone number of the school.
        fax_number (models.CharField, optional): The fax number of the school (optional).
        email (models.EmailField): The email address of the school (unique).
        website (models.URLField, optional): The website URL of the school (optional).
        city (models.CharField): The city where the school is located.
        street (models.CharField): The street where the school is located.
        building_number (models.CharField): The building number of the school.
        apartment_number (models.CharField, optional): The apartment number of the school (optional).
        postcode (models.CharField): The postcode of the school.

    Meta:
        db_table (str): The database table name for the School model.

    Methods:
        __str__(): Returns a string representation of the school.

    Example:
        school = School(name='Example School', phone_number='123-456-7890', email='example@example.com',
                        city='Cityville', street='Main Street', building_number='123', postcode='ABCDE')
        school.save()
    """
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
        """
        Returns a string representation of the school.

        Returns:
            str: The name of the school.
        """
        return self.name


class User(AbstractBaseUser):
    """
    Custom user model representing individuals in the system.

    Attributes:
        email (models.EmailField): The unique email address associated with the user.
        first_name (models.CharField): The first name of the user.
        last_name (models.CharField): The last name of the user.
        created_at (models.DateTimeField): The timestamp indicating when the user was created.
        school (models.ForeignKey, optional): The associated school for the user (optional, set to NULL).
        user_type (models.CharField): The type of user (choices from UserType enum, default is UserType.USER).

    Meta:
        db_table (str): The database table name for the User model.

    Constants:
        USERNAME_FIELD (str): The field used for authentication (email in this case).
        objects (CustomUserManager): The custom manager for the User model.

    Properties:
        is_admin (bool): Returns True if the user is of type ADMIN, False otherwise.
        is_user (bool): Returns True if the user is of type USER, False otherwise.
        is_observer (bool): Returns True if the user is of type OBSERVER, False otherwise.

    Methods:
        clean(): Ensures the user instance is valid, raising a ValidationError if any issues are found.
        save(*args, **kwargs): Overrides the default save method to perform additional actions before saving.

    Example:
        user = User(email='user@example.com', first_name='John', last_name='Doe', user_type=UserType.USER)
        user.save()
    """
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
        """
        Checks if the user is of type ADMIN.

        Returns:
            bool: True if the user is of type ADMIN, False otherwise.
        """
        return self.user_type == UserType.ADMIN.value

    @property
    def is_user(self):
        """
        Checks if the user is of type USER.

        Returns:
            bool: True if the user is of type USER, False otherwise.
        """
        return self.user_type == UserType.USER.value

    @property
    def is_observer(self):
        """
        Checks if the user is of type OBSERVER.

        Returns:
            bool: True if the user is of type OBSERVER, False otherwise.
        """
        return self.user_type == UserType.OBSERVER.value

    def clean(self):
        """
        Validates the user instance.

        Raises:
            ValidationError: If the user instance is not valid.
        """
        super().clean()

        valid_user_types = [tag.value for tag in UserType]
        if self.user_type not in valid_user_types:
            raise ValidationError("Invalid user type.")

        if self.user_type != UserType.USER.value and self.school is not None:
            raise ValidationError(
                "Only users with type 'USER' can have a school.")

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to perform additional actions before saving.

        Raises:
            ValidationError: If an attempt is made to update the user_type field.
        """
        if self.id:  # Check if the instance is already saved (updating)
            original_user = User.objects.get(id=self.id)
            if self.user_type != original_user.user_type:
                raise ValidationError("Cannot update user_type field.")

        self.full_clean()
        super().save(*args, **kwargs)


class PendingApproval(models.Model):
    """
    Represents a pending approval request for a user to join a school.

    Attributes:
        user (models.ForeignKey): The user requesting approval to join a school.
        school (models.ForeignKey): The school to which the user is requesting approval.

    Methods:
        __str__(): Returns a string representation of the pending approval instance.

    Meta:
        db_table (str): The database table name for the PendingApproval model.

    Example:
        user = User.objects.get(email='user@example.com')
        school = School.objects.get(name='Example School')
        approval_request = PendingApproval(user=user, school=school)
        approval_request.save()
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the pending approval instance.

        Returns:
            str: A formatted string indicating the pending approval details.
        """
        return f"Pending Approval: user: {self.user}, school: {self.school}"

    class Meta:
        db_table = 'pending_approval'
