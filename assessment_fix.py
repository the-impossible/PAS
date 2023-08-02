from PAS_assessment.models import Assessment, ProjectAssessment, SeminarAssessment

for obj in Assessment.objects.all():
    if obj.project_defense_grade or obj.supervisor_grade:
        ProjectAssessment.objects.create(
            student_id=obj.student_id,
            assessor_id=obj.assessor_id,
            supervisor=obj.supervisor,
            prog_id=obj.prog_id,
            sess_id=obj.sess_id,
            type_id=obj.type_id,
            dept_id=obj.dept_id,
            project_defense_grade=obj.project_defense_grade,
            supervisor_grade=obj.supervisor_grade,
            created=obj.created
        )

for obj in Assessment.objects.all():

    if obj.seminar_defense_grade:
        SeminarAssessment.objects.create(
            student_id=obj.student_id,
            assessor_id=obj.assessor_id,
            prog_id=obj.prog_id,
            sess_id=obj.sess_id,
            type_id=obj.type_id,
            dept_id=obj.dept_id,
            seminar_defense_grade=obj.seminar_defense_grade,
            created=obj.created
        )