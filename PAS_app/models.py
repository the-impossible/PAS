# My Django imports
from django.db import models
import uuid, os
from django.utils.deconstruct import deconstructible
import uuid

# My App imports

# Create your models here.
class Session(models.Model):
    session_title = models.CharField(max_length=9, unique=True)
    session_description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.session_title

    class Meta:
        db_table = 'Session'
        verbose_name_plural = 'Sessions'

class Department(models.Model):
    dept_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    dept_title = models.CharField(max_length=30, unique=True)
    dept_desc = models.CharField(max_length=100, blank=True, null=True)
    dept_logo = models.ImageField(upload_to='uploads/department/', blank=True, null=True)

    def __str__(self):
        return self.dept_title

    class Meta:
        db_table = 'Department'
        verbose_name_plural = 'Departments'

class Programme(models.Model):
    programme_title = models.CharField(max_length=30, unique=True)
    programme_description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.programme_title

    class Meta:
        db_table = 'Programme'
        verbose_name_plural = 'Programmes'

class StudentType(models.Model):
    type_title = models.CharField(max_length=30, unique=True)
    type_description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.type_title

    class Meta:
        db_table = 'StudentType'
        verbose_name_plural = 'Student Types'

def path_and_rename(instance, filename):
    path = 'uploads/csv/'
    ext = filename.split('.')[-1]
    filename = f'{instance.programme}_{instance.student_type}.{ext}'
    return f'{path}{filename}'

class Files(models.Model):
    file = models.FileField(upload_to=path_and_rename)
    session = models.ForeignKey(to=Session, on_delete=models.CASCADE)
    programme = models.ForeignKey(to=Programme, on_delete=models.CASCADE)
    dept = models.ForeignKey(to=Department, on_delete=models.CASCADE)
    student_type = models.ForeignKey(to=StudentType, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.file}'

    def delete(self, using=None, keep_parents=False):
        self.file.storage.delete(self.file.name)
        super().delete()

    class Meta:
        db_table = 'File'
        verbose_name_plural = 'Files'

class SupervisorRank(models.Model):
    rank_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    rank_description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.rank_description}'
    class Meta:
        db_table = 'Supervisor Rank'
        verbose_name_plural = 'Supervisor Rank'

def path_and_rename_super(instance, filename):
    path = 'uploads/csv/'
    ext = filename.split('.')[-1]
    filename = f'Supervisors.{ext}'
    return f'{path}{filename}'

class SupervisorsFiles(models.Model):
    file = models.FileField(upload_to=path_and_rename_super)
    dept = models.ForeignKey(to=Department, on_delete=models.CASCADE)
    prog = models.ForeignKey(to=Programme, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.file}'

    def delete(self, using=None, keep_parents=False):
        self.file.storage.delete(self.file.name)
        super().delete()

    class Meta:
        db_table = 'Supervisors File'
        verbose_name_plural = 'Supervisors Files'

class Title(models.Model):
    title_number = models.CharField(max_length=10, unique=True)
    title_description = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.title_description}'
    class Meta:
        db_table = 'Supervisor Title'
        verbose_name_plural = 'Supervisor Title'