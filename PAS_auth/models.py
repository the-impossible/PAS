# My Django imports
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid

# My app imports

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, firstname, lastname, password=None):

        #creates a user with the parameters
        if not username:
            raise ValueError('Username is required!')

        if not firstname:
            raise ValueError('First Name is required!')

        if not lastname:
            raise ValueError('Last Name is required!')

        if password is None:
            raise ValueError('Password is required!')

        user = self.model(
            username=username.upper().strip(),
            firstname=firstname.title().strip(),
            lastname=lastname.title().strip(),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, firstname, lastname, password=None):
        # create a superuser with the above parameters
        if not username:
            raise ValueError('Username is required!')

        if not firstname:
            raise ValueError('First Name is required!')

        if not lastname:
            raise ValueError('Last Name is required!')

        if password is None:
            raise ValueError('Password should not be empty')

        user = self.create_user(
            username=username,
            firstname=firstname,
            lastname=lastname,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    username = models.CharField(max_length=20, db_index=True, unique=True, blank=True)
    firstname = models.CharField(max_length=20, db_index=True, blank=True)
    lastname = models.CharField(max_length=20, db_index=True, blank=True)
    phone = models.CharField(max_length=11, db_index=True, unique=True, blank=True)
    email = models.CharField(max_length=100, db_index=True, unique=True, verbose_name='email address', blank=True)

    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    has_changed = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['firstname', 'lastname',]

    objects = UserManager()

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def get_fullname(self):
        return f'{self.lastname} {self.firstname}'

    def __str__(self):
        return f'{self.username.upper()}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'
