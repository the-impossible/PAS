from django.db import models
import uuid

from PAS_auth.models import (
    Programme,
    Session,
    Department,
    StudentType,
    StudentProfile,
    SupervisorProfile,
)

# Create your models here.

class Venue(models.Model):
    venue_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    venue_title = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now=True)
    prog_id = models.ForeignKey(Programme, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.venue_title} | {self.prog_id}'

    class Meta:
        db_table = 'Venues'
        verbose_name_plural = 'Venues'

class DaysOfDefense(models.Model):
    days_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    num_of_day = models.IntegerField(default=3)
    date_created = models.DateTimeField(auto_now=True)
    prog_id = models.ForeignKey(Programme, on_delete=models.CASCADE)
    sess_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    type_id = models.ForeignKey(StudentType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sess_id} - {self.dept_id} : {self.num_of_day}days'

    class Meta:
        db_table = 'Days Of Defense'
        verbose_name_plural = 'Days Of Defenses'

class StudHallAllocation(models.Model):
    studHall_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)
    stud_id = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    day_num = models.IntegerField(default=1)
    sess_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    prog_id = models.ForeignKey(Programme, on_delete=models.CASCADE)
    type_id = models.ForeignKey(StudentType, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.stud_id} is allocated to: {self.venue_id} on day {self.day_num}'

    class Meta:
        db_table = 'Student Hall Allocation'
        verbose_name_plural = 'Student Hall Allocations'

class AssessorHallAllocation(models.Model):
    assessHall_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)
    assessor_one = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE, related_name='assessor_one')
    assessor_two = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE, related_name='assessor_two')
    chief_assessor = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE)
    sess_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    type_id = models.ForeignKey(StudentType, on_delete=models.CASCADE)
    prog_id = models.ForeignKey(Programme, on_delete=models.CASCADE)

    def __str__(self):
        return f'CHIEF: {self.chief_assessor} | ONE: {self.assessor_one} | TWO: {self.assessor_two}'

    class Meta:
        db_table = 'Assessor Hall Allocation'
        verbose_name_plural = 'Assessors Hall Allocations'



