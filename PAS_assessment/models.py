from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

from PAS_auth.models import (
    Programme,
    Session,
    Department,
    StudentProfile,
    SupervisorProfile,
    StudentType,
)

from PAS_hallAllocation.models import (
    StudHallAllocation,
    Venue,
)

# Create your models here.
class Assessment(models.Model):
    assess_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    student_id = models.ForeignKey(StudHallAllocation, on_delete=models.CASCADE)

    assessor_id = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE, null=True, blank=True)
    supervisor = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="supervisor_assessment")
    # project_assessor = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE, null=True, blank=True)

    prog_id = models.ForeignKey(Programme, on_delete=models.CASCADE)
    sess_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    type_id = models.ForeignKey(StudentType, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    seminar_defense_grade = models.IntegerField(default=0)
    project_defense_grade = models.IntegerField(default=0)
    supervisor_grade = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def current_grade(self):
        return self.seminar_defense_grade + self.project_defense_grade + self.supervisor_grade

    def total_defense_grade(self):
        return self.project_defense_grade + self.supervisor_grade

    def __str__(self):
        return f'{self.student_id} - {self.current_grade}'

    class Meta:
        db_table = 'Assessment'
        verbose_name_plural = 'Assessments'

class SeminarAssessment(models.Model):
    assess_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True, blank=True)

    student_id = models.ForeignKey(StudHallAllocation, on_delete=models.CASCADE)
    assessor_id = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE, null=True, blank=True)

    prog_id = models.ForeignKey(Programme, on_delete=models.CASCADE)
    sess_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    type_id = models.ForeignKey(StudentType, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)

    seminar_defense_grade = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100, message="Grade can't be more than 100")])
    created = models.DateTimeField(auto_now_add=True)

    @property
    def current_grade(self):
        return self.seminar_defense_grade

    def total_defense_grade(self):
        return self.project_defense_grade

    def __str__(self):
        return f'{self.student_id} - {self.current_grade}'

    class Meta:
        db_table = 'Seminar Assessment'
        verbose_name_plural = 'Seminar Assessments'

class ProjectAssessment(models.Model):
    assess_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True, blank=True)

    student_id = models.ForeignKey(StudHallAllocation, on_delete=models.CASCADE)
    assessor_id = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="project_assessor")

    supervisor = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="student_supervisor")

    prog_id = models.ForeignKey(Programme, on_delete=models.CASCADE)
    sess_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    type_id = models.ForeignKey(StudentType, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)

    project_defense_grade = models.IntegerField(default=0,  validators=[MinValueValidator(0), MaxValueValidator(50, message="Grade can't be more than 50")])
    supervisor_grade = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(50, message="Grade can't be more than 50")])
    created = models.DateTimeField(auto_now_add=True)

    @property
    def current_grade(self):
        return self.project_defense_grade + self.supervisor_grade

    def total_defense_grade(self):
        return self.project_defense_grade + self.supervisor_grade

    def __str__(self):
        return f'{self.student_id} - {self.current_grade}'

    class Meta:
        db_table = 'Project Assessment'
        verbose_name_plural = 'Project Assessments'

