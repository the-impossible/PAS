# My Django Imports
from django import forms
from django.core.exceptions import ValidationError

# My App imports
from PAS_hallAllocation.models import (
    Venue,
    DaysOfDefense,
    StudHallAllocation,
    AssessorHallAllocation,
)
from PAS_app.models import (
    Programme,
    Department,
    Session,
    StudentType,
)

from PAS_auth.models import (
    StudentProfile,
    SupervisorProfile,
)

from PAS_assessment.models import (
    Assessment
)

class SeminarAssessmentForm(forms.ModelForm):

    student_id = forms.ModelChoiceField(queryset=StudHallAllocation.objects.all(), empty_label="(Select Student)", help_text="Select Student", required=True, widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    seminar_defense_grade = forms.CharField(help_text='Enter seminar defense grade', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number'
        }
    ))

    def __init__(self, *args, **kwargs):
        self.assessor = kwargs.pop('assessor', '')
        super(SeminarAssessmentForm, self).__init__(*args, **kwargs)
        self.fields['student_id'].queryset=StudHallAllocation.objects.filter(venue_id=self.assessor.venue_id, dept_id=self.assessor.dept_id, prog_id=self.assessor.prog_id, type_id=self.assessor.type_id)
        self.fields['student_id'].widget.attrs['style'] = 'width:280px;'

    def clean(self):
        seminar_grade = int(self.cleaned_data.get('seminar_defense_grade'))
        student_id = self.cleaned_data.get('student_id')

        if seminar_grade > 100:
            raise ValidationError('Maximum grade is 100, try again!')

        if seminar_grade < 0:
            raise ValidationError('Positive grades only, try again!')

        check = Assessment.objects.filter(student_id=student_id, dept_id=self.assessor.dept_id, type_id=self.assessor.type_id, prog_id=self.assessor.prog_id, sess_id=self.assessor.sess_id)

        if self.instance:
            check = check.exclude(pk=self.instance.pk)

        if check.exists():
            existing_seminar_grade = check.get(student_id=student_id, dept_id=self.assessor.dept_id, type_id=self.assessor.type_id, prog_id=self.assessor.prog_id, sess_id=self.assessor.sess_id).seminar_defense_grade

            if seminar_grade == 0:
                raise ValidationError("Default grade is zero, simply don't grade if grade is zero")

            if existing_seminar_grade > 0:
                raise ValidationError('Assessment already exist for the student try editing!')


    class Meta:
        model = Assessment
        fields = ('student_id', 'seminar_defense_grade')

class ProjectAssessmentForm(forms.ModelForm):

    student_id = forms.ModelChoiceField(queryset=StudHallAllocation.objects.all(), empty_label="(Select Student)", help_text="Select Student", required=True, widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    project_defense_grade = forms.CharField(help_text='Enter project defense grade', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number'
        }
    ))

    def __init__(self, *args, **kwargs):
        self.assessor = kwargs.pop('assessor', '')
        super(ProjectAssessmentForm, self).__init__(*args, **kwargs)
        self.fields['student_id'].queryset=StudHallAllocation.objects.filter(venue_id=self.assessor.venue_id, dept_id=self.assessor.dept_id, prog_id=self.assessor.prog_id, type_id=self.assessor.type_id)
        self.fields['student_id'].widget.attrs['style'] = 'width:280px;'

    def clean(self):
        project_grade = int(self.cleaned_data.get('project_defense_grade'))
        student_id = self.cleaned_data.get('student_id')

        if project_grade > 60:
            raise ValidationError('Maximum grade is 60, try again!')

        if project_grade < 0:
            raise ValidationError('Positive grades only, try again!')

        check = Assessment.objects.filter(student_id=student_id, dept_id=self.assessor.dept_id, type_id=self.assessor.type_id, prog_id=self.assessor.prog_id, sess_id=self.assessor.sess_id)

        if self.instance:
            check = check.exclude(pk=self.instance.pk)


        if check.exists():

            existing_project_grade = check.get(student_id=student_id, dept_id=self.assessor.dept_id, type_id=self.assessor.type_id, prog_id=self.assessor.prog_id, sess_id=self.assessor.sess_id).project_defense_grade

            if project_grade == 0:
                raise ValidationError("Default grade is zero, simply don't grade if grade is zero")

            if existing_project_grade > 0:
                raise ValidationError('Assessment already exist for the student try editing!')



    class Meta:
        model = Assessment
        fields = ('student_id', 'project_defense_grade')


class ProgrammeTypeSelectionForm(forms.Form):

    student_type = forms.ModelChoiceField(queryset=StudentType.objects.all(), empty_label="(Select Student Programme Type)", required=True, help_text="Select Student Programme Type", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    session = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", required=True, help_text="Select Session", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))


class SuperSeminarAssessmentForm(forms.ModelForm):

    student_id = forms.ModelChoiceField(queryset=StudHallAllocation.objects.all(), empty_label="(Select Student)", help_text="Select Student", widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    seminar_defense_grade = forms.CharField(help_text='Enter seminar defense grade', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number'
        }
    ))

    def __init__(self, *args, **kwargs):
        self.dept_id = Department.objects.get(dept_id=kwargs.pop('dept_id', ''))
        self.type_id = StudentType.objects.get(id=kwargs.pop('type_id', ''))
        self.prog_id = Programme.objects.get(id=kwargs.pop('prog_id', ''))
        self.sess_id = Session.objects.get(id=kwargs.pop('sess_id', ''))

        super(SuperSeminarAssessmentForm, self).__init__(*args, **kwargs)
        self.fields['student_id'].queryset=StudHallAllocation.objects.filter(dept_id=self.dept_id, prog_id=self.prog_id, type_id=self.type_id)
        self.fields['student_id'].widget.attrs['style'] = 'width:280px;'

    def clean(self):
        seminar_grade = int(self.cleaned_data.get('seminar_defense_grade'))
        student_id = self.cleaned_data.get('student_id')

        if seminar_grade > 100:
            raise ValidationError('Maximum grade is 100, try again!')

        if seminar_grade < 0:
            raise ValidationError('Positive grades only, try again!')

        check = Assessment.objects.filter(student_id=student_id, dept_id=self.dept_id, type_id=self.type_id, prog_id=self.prog_id, sess_id=self.sess_id)

        if self.instance:
            check = check.exclude(pk=self.instance.pk)

        if check.exists():
            raise ValidationError('Assessment already exist for the student try editing!')

    class Meta:
        model = Assessment
        fields = ('student_id', 'seminar_defense_grade')
