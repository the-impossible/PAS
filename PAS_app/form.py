# My Django Imports
from django import forms
import csv
# My App imports
from PAS_app.models import (
    Session,
    Programme,
    StudentType,
    SupervisorsFiles,
    Files,
)

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


    def clean(self):
        cleaned_data = super().clean()

        session = cleaned_data.get('session')
        programme = cleaned_data.get('programme')
        student_type = cleaned_data.get('student_type')
        file = self.cleaned_data.get('file')

        with open(f'{file}', 'r') as file:
            csv_obj = csv.reader(file)
            next(csv_obj)

            for col in csv_obj:
                if len(col) != 6:raise forms.ValidationError('Invalid CSV FILE')
                for row in col:
                    if row == '':raise forms.ValidationError('Invalid CSV')

        check = Files.objects.filter(session=session, programme=programme, student_type=student_type)

        if check.exists():
            raise forms.ValidationError('File has been added previously for the info provided!')

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

    def clean(self):
        cleaned_data = super().clean()
        file = self.cleaned_data.get('file')

        with open(f'{file}', 'r') as file:
            csv_obj = csv.reader(file)
            next(csv_obj)

            for col in csv_obj:
                if len(col) != 7:raise forms.ValidationError('Invalid CSV FILE')
                for row in col:
                    if row == '':raise forms.ValidationError('Invalid CSV')

    class Meta:
        model = SupervisorsFiles
        fields = ('file',)
