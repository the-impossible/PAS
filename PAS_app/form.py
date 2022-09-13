# My Django Imports
from django import forms
import csv, io
# My App imports
from PAS_app.models import (
    Session,
    Programme,
    Department,
    StudentType,
    SupervisorsFiles,
    Files,
    SupervisorRank,
)

from PAS_auth.models import (
    User,
    Groups,
    StudentProfile,
    SupervisorProfile,
    Coordinators,
    Session,
    Allocate,
)

class FileHandler:
    def __init__(self, obj):
        self.csv_obj = obj

    def validate_stud_file(self):
        for col in self.csv_obj:
            existing_users = User.objects.filter(username=col[0])
            if len(col) != 3:raise forms.ValidationError('Invalid CSV FILE')
            for row in col:
                if row == '':raise forms.ValidationError('Invalid CSV')

            if existing_users.exists():
                raise forms.ValidationError('File contains already registered registration numbers!')


    def validate_super_file(self):
        for col in self.csv_obj:
            existing_users = User.objects.filter(username=col[0])
            if len(col) != 4:raise forms.ValidationError('Invalid CSV FILE')
            for row in col:
                if row == '':raise forms.ValidationError('Invalid CSV')

            if existing_users.exists():
                raise forms.ValidationError('File contains already registered registration numbers!')

class FilesForm(forms.ModelForm):

    file = forms.FileField(help_text='Select Student CSV file',widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'.csv'
        }
    ))

    session = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", required=True, help_text="Select academic session", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    programme = forms.ModelChoiceField(queryset=Programme.objects.all(), empty_label="(Select Programme)", required=True, help_text="Select academic programme", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    student_type = forms.ModelChoiceField(queryset=StudentType.objects.all(), empty_label="(Select Student type)", required=True, help_text="Select either Regular or Evening", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    def __init__(self, *args, **kwargs):
        self.dept_id = kwargs.pop('dept_id', '')
        super(FilesForm, self).__init__(*args, **kwargs)


    def clean_file(self):
        cleaned_data = super().clean()

        session = cleaned_data.get('session')
        programme = cleaned_data.get('programme')
        student_type = cleaned_data.get('student_type')
        file = io.TextIOWrapper(cleaned_data.get('file').file)

        csv_obj = csv.reader(file)
        next(csv_obj)

        handler = FileHandler(csv_obj)
        handler.validate_stud_file()

        check = Files.objects.filter(session=session, programme=programme, student_type=student_type, dept=self.dept_id)

        if check.exists():
            raise forms.ValidationError('File has been added previously for the info provided!')

        return file

    class Meta:
        model = Files
        fields = ('file', 'session', 'programme', 'student_type')

class SuperFilesForm(forms.ModelForm):
    file = forms.FileField(help_text='Select Supervisor CSV file', widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'.csv'
        }
    ))

    def __init__(self, *args, **kwargs):
        self.dept_id = kwargs.pop('dept_id', '')
        super(SuperFilesForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        cleaned_data = super().clean()
        file = io.TextIOWrapper(cleaned_data.get('file').file)

        csv_obj = csv.reader(file)
        next(csv_obj)

        handler = FileHandler(csv_obj)
        handler.validate_super_file()

        return file

    class Meta:
        model = SupervisorsFiles
        fields = ('file',)

class StudentProfileForm(forms.ModelForm):

    student_type = forms.ModelChoiceField(queryset=StudentType.objects.all(), empty_label="(Select Student Category)", required=True, help_text="Select either Regular or Evening", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    session = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", required=True, help_text="Select academic session", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    programme = forms.ModelChoiceField(queryset=Programme.objects.all(), empty_label="(Select Programme)", required=True, help_text="Select academic programme", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    class Meta:
        model = StudentProfile
        fields = ('session', 'programme', 'student_type')

class MultipleSuperForm(forms.Form):
    file = forms.FileField(help_text='Select CSV file',widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'.csv'
        }
    ))

    def clean_file(self):
        file = io.TextIOWrapper(self.cleaned_data.get('file').file)

        csv_obj = csv.reader(file)
        next(csv_obj)

        handler = FileHandler(csv_obj)
        handler.validate_super_file()

        return file

class MultipleStudentForm(forms.Form):
    file = forms.FileField(help_text='Select Student CSV file',widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'.csv'
        }
    ))

    session = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", required=True, help_text="Select academic session", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    programme = forms.ModelChoiceField(queryset=Programme.objects.all(), empty_label="(Select Programme)", required=True, help_text="Select academic programme", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    student_type = forms.ModelChoiceField(queryset=StudentType.objects.all(), empty_label="(Select Student type)", required=True, help_text="Select either Regular or Evening", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    def clean_file(self):

        file = io.TextIOWrapper(self.cleaned_data.get('file').file)

        csv_obj = csv.reader(file)
        next(csv_obj)

        handler = FileHandler(csv_obj)
        handler.validate_stud_file()

        return file

class SupervisorProfileForm(forms.ModelForm):

    rank_id = forms.ModelChoiceField(queryset=SupervisorRank.objects.all(), empty_label="(Select Supervisor Rank)", required=True, help_text="Select either level from the dropdown list", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    class Meta:
        model = SupervisorProfile
        fields = ('rank_id',)

class CoordinatorsForm(forms.ModelForm):

    prog_id = forms.ModelChoiceField(queryset=Programme.objects.all(), empty_label="(Select Programme)", help_text="Select academic programme", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    chief_coord_id = forms.ModelChoiceField(required=False, queryset=SupervisorProfile.objects.all(), empty_label="(Select Chief Coordinator)", help_text="Select Chief Coordinator", widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    asst_coord_id = forms.ModelChoiceField(queryset=SupervisorProfile.objects.all(), empty_label="(Select Asst Coordinator)", required=False, help_text="Select Asst Coordinator", widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    def __init__(self, dept_id, *args, **kwargs):
        super(CoordinatorsForm, self).__init__(*args, **kwargs)
        self.fields['chief_coord_id'].queryset=SupervisorProfile.objects.filter(dept_id=dept_id)
        self.fields['asst_coord_id'].queryset=SupervisorProfile.objects.filter(dept_id=dept_id)
        self.fields['asst_coord_id'].widget.attrs['style'] = 'width:400px;'
        self.fields['chief_coord_id'].widget.attrs['style'] = 'width:400px;'

    class Meta:
        model = Coordinators
        fields = ('chief_coord_id', 'asst_coord_id', 'prog_id')

class AllocationForm(forms.ModelForm):

    prog_id = forms.ModelChoiceField(queryset=Programme.objects.all(), empty_label="(Select Programme)", help_text="Select academic programme", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    sess_id = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", help_text="Select Academic Session", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    type_id = forms.ModelChoiceField(queryset=StudentType.objects.all(), empty_label="(Select Student Category)", help_text="Select Category of Student", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    class Meta:
        model = Allocate
        fields = ('sess_id', 'prog_id')

class MAllocationForm(forms.ModelForm):

    group_id = forms.ModelChoiceField(queryset=Groups.objects.all(), empty_label="(Select Group)", help_text="Select Academic Group", widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    sess_id = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", help_text="Select Academic Session", widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    stud_id = forms.ModelChoiceField(queryset=StudentProfile.objects.all(), empty_label="(Select Student)", help_text="Select Student", widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    super_id = forms.ModelChoiceField(queryset=SupervisorProfile.objects.all(), empty_label="(Select Supervisor)", help_text="Select Supervisor", widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    def __init__(self, *args, **kwargs):
        self.dept_id = kwargs.pop('dept_id', '')
        super(MAllocationForm, self).__init__(*args, **kwargs)
        self.fields['stud_id'].queryset=StudentProfile.objects.filter(dept_id=self.dept_id)
        self.fields['super_id'].queryset=SupervisorProfile.objects.filter(dept_id=self.dept_id)
        self.fields['group_id'].widget.attrs['style'] = 'width:400px;'
        self.fields['stud_id'].widget.attrs['style'] = 'width:400px;'
        self.fields['super_id'].widget.attrs['style'] = 'width:400px;'
        self.fields['sess_id'].widget.attrs['style'] = 'width:400px;'

    class Meta:
        model = Allocate
        fields = ('sess_id', 'group_id', 'stud_id', 'super_id')

class RAllocationForm(forms.ModelForm):

    sess_id = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", help_text="Select Academic Session", widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    prog_id = forms.ModelChoiceField(queryset=Programme.objects.all(), empty_label="(Select Programme)", help_text="Select Student", widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    type_id = forms.ModelChoiceField(queryset=StudentType.objects.all(), empty_label="(Select Student Category)", help_text="Select Student Category", widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    class Meta:
        model = Allocate
        fields = ('sess_id', 'prog_id', 'type_id')

class DepartmentForm(forms.ModelForm):

    dept_title = forms.CharField(help_text='Please enter department title',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    dept_desc = forms.CharField(help_text='Please enter department description',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    dept_logo = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'image/png, image/jpeg'
        }
    ))

    class Meta:
        model = Department
        fields = ('dept_title', 'dept_desc', 'dept_logo')



