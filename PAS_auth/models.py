# My Django imports
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid

# My app imports
from PAS_app.models import (
    Programme,
    Department,
    Session,
    StudentType,
    SupervisorRank,
    Title,
)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None):

        #creates a user with the parameters
        if not username:
            raise ValueError('Username is required!')

        if not name:
            raise ValueError('Fullname is required!')

        if password is None:
            raise ValueError('Password is required!')

        user = self.model(
            username=username.upper().strip(),
            name=name.title().strip(),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, name, password=None):
        # create a superuser with the above parameters
        if not username:
            raise ValueError('Username is required!')

        if not name:
            raise ValueError('Fullname is required!')

        if password is None:
            raise ValueError('Password should not be empty')

        user = self.create_user(
            username=username,
            name=name,
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
    name = models.CharField(max_length=60, db_index=True, blank=True)
    phone = models.CharField(max_length=11, db_index=True, unique=True, blank=True, null=True)
    pic = models.ImageField(default='img/comlogo.png', null=True, blank=True, upload_to='uploads/profile/')
    email = models.CharField(max_length=100, db_index=True, unique=True, verbose_name='email address', blank=True, null=True)

    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_super = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['name',]

    objects = UserManager()

    def get_fullname(self):
        if self.is_super:
            return f'{SupervisorProfile.objects.get(user_id=self.user_id).title} {self.name}'
        return f'{self.name}'

    def has_updated(self):
        return self.is_verified

    def __str__(self):
        return f'{self.username.upper()}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'

class StudentProfile(models.Model):
    stud_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user_id = models.OneToOneField(User,blank=True, null=True, on_delete=models.CASCADE)
    programme_id = models.ForeignKey(Programme, on_delete=models.CASCADE)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    type_id = models.ForeignKey(StudentType, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id}'

    class Meta:
        db_table = 'Student Profile'
        verbose_name_plural = 'Student Profile'

class SupervisorProfile(models.Model):
    super_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rank_id = models.ForeignKey(SupervisorRank, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    prog_id = models.ForeignKey(Programme, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    RG_capacity = models.CharField(max_length=10, default=0)
    Ev_capacity = models.CharField(max_length=10, default=0)

    def __str__(self):
        return f'{self.user_id}: {self.user_id.get_fullname()}'

    class Meta:
        db_table = 'Supervisor Profile'
        verbose_name_plural = 'Supervisor Profile'

class Coordinators(models.Model):
    chief_coord_id = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE, related_name='chief_coord')
    asst_coord_id = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE, related_name='asst_coord')
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    prog_id = models.ForeignKey(Programme, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.dept_id} {self.prog_id} coordinators'

    class Meta:
        db_table = 'Coordinator Details'
        verbose_name_plural = 'Coordinators Details'

class Groups(models.Model):
    group_num = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.group_num}'

    class Meta:
        db_table = 'Groups'
        verbose_name_plural = 'Groups'

class Allocate(models.Model):
    allocate_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE)
    sess_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    prog_id = models.ForeignKey(Programme, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    stud_id = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    type_id = models.ForeignKey(StudentType, on_delete=models.CASCADE)
    super_id = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.stud_id} is allocated to {self.super_id} with group number of {self.group_id}'

    class Meta:
        db_table = 'Allocation Details'
        verbose_name_plural = 'Allocation Details'

class EmailSendCount(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    count = models.IntegerField(default=0)

    @property
    def increaseCount(self):
        self.count += 1

    @property
    def resetCount(self):
        self.count = 0

    @property
    def getCount(self):
        return self.count

    def __str__(self):
        return f'{self.user}, has used ({self.count})/({10})'

    class Meta:
        db_table = 'EmailCounter'

