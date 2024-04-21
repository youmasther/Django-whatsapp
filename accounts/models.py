from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from core.models  import Messages
# Create your models here.

# The `MyAccountManager` class is a custom user manager in Python that provides methods for creating
# regular users and superusers with specific attributes.
class MyAccountManager(BaseUserManager):
    """docstring for MyAccountManager"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('L\'adresse email est obligatoire')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)
    
def get_profile_image_filepath(self, filename):
    """
    The function `get_profile_image_filepath` returns the file path for a user's profile image based on
    their ID and the provided filename.
    
    :param filename: The `filename` parameter in the `get_profile_image_filepath` function represents
    the name of the image file that you want to save or retrieve. It will be used to construct the file
    path where the image will be stored or retrieved from
    :return: a string that represents the file path for a user's profile image. The file path includes
    the user's id and the filename provided as input to the function.
    """
    return f'image_de_profiles/user_{self.id}/{filename}'

def get_default_profile_image():
    """
    The function `get_default_profile_image` returns the default profile image path
    'image_de_profiles/avatar-1.png'.
    :return: 'image_de_profiles/avatar-1.png'
    """
    return 'image_de_profiles/avatar-1.png'

# This Python class defines an Account model with fields for personal information, login details,
# permissions, and a profile image.
class User(AbstractBaseUser):
    prenom = models.CharField(max_length=100, null=True, blank=True)
    nom = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=65,verbose_name="email", unique=True)
    date_joined = models.DateTimeField(verbose_name='date de creation', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="dernier connexion", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    objects = MyAccountManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "User"

    # USERNAME_FIELD = 'email'
    def __str__(self):
        return '{} {}'.format(self.prenom, self.nom)
    
    @property
    def last_message(self):
        return Messages.objects.filter(sender=self).last()

    def get_profile_image_filename(self):
	    return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{str(pk)}'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
	    return True
    

def get_media_file(instance, filename):
    """
    The function `get_media_file` returns the file path for a media file based on the instance ID and
    filename provided.
    
    :param instance: Instance refers to an instance of a model or class in object-oriented programming.
    In this context, it likely represents an instance of a media file object or entity that is being
    processed or handled within the code snippet provided
    :param filename: The `filename` parameter is a string that represents the name of the file being
    processed or accessed. It could be the name of an image file, video file, audio file, or any other
    type of media file
    :return: The function `get_media_file` is returning a string that represents the file path for a
    media file. The file path is constructed by joining the elements 'images', the ID of the instance,
    and the filename using the '/' separator.
    """
    return '/'.join(['images', str(instance.id),filename])


class Messages(models.Model):
    sender = models.ForeignKey(User, related_name=("sender"), on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name=("receiver"), on_delete=models.CASCADE)
    content = models.TextField()
    media_url = models.ImageField(max_length=255, upload_to=get_media_file, null=True, blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Messages"
        verbose_name_plural = "Messages"
        db_table = "Messages"

    def __str__(self):
        return f"Message {self.id} - {self.content[:20]}"