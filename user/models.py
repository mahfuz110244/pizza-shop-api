from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, password=None, **kwargs):
        if not kwargs.get('username'):
            raise ValueError('Users must have a valid phone')

        user = self.model(
            username=kwargs.get('username'),
            email=kwargs.get('email', None),
            image=kwargs.get('image', None),
            name=kwargs.get('full_name', None),
            address=kwargs.get('address', None),
            latitude=kwargs.get('latitude', None),
            longitude=kwargs.get('longitude', None)
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, password=None, **kwargs):
        user = self.model(
            username=kwargs.get('username')
        )

        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=14, verbose_name='Phone')
    name = models.CharField(max_length=256, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    latitude = models.FloatField(max_length=50, blank=True, null=True, default=0)
    longitude = models.FloatField(max_length=50, blank=True, null=True, default=0)
    email = models.EmailField(blank=True, null=True)
    image = models.FileField(upload_to='uploads/profile/', default="/profile_picture.png", blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    @property
    def get_short_name(self):
        return self.username

    def __str__(self):
        return f"{self.id} - {self.username}"

    class Meta:
        db_table = 'customer'
        verbose_name_plural = '01. Customers'
        # ordering = ['name']
