from django.db import models
import uuid

from PAS_auth.models import (
    Programme,
    Session,
    Department,
    StudentProfile,
    SupervisorProfile,
)

# Create your models here.
class Assessment(models.Model):
    assess_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    student_id = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    assessor_id = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE)
    prog_id = models.ForeignKey(Programme, on_delete=models.CASCADE)
    sess_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    seminar_defense_grade = models.IntegerField(default=0)
    project_defense_grade = models.IntegerField(default=0)
    supervisor_grade = models.IntegerField(default=0)

    @property
    def current_grade(self):
        return self.seminar_defense_grade + self.project_defense_grade + self.supervisor_grade

    def __str__(self):
        return f'{self.student_id} - {self.current_grade}'

    class Meta:
        db_table = 'Assessment'
        verbose_name_plural = 'Assessments'
