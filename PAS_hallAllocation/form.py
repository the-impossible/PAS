# My Django Imports
from django import forms
from django.core.exceptions import ValidationError

# My App imports
from PAS_hallAllocation.models import (
    Venue,
    DaysOfDefense,
    StudHallAllocation,
)
from PAS_app.models import (
    Programme,
    Department,
    Session,
    StudentType,
)

from PAS_auth.models import (
    StudentProfile,
)

class VenueForm(forms.ModelForm):
    venue_title = forms.CharField(help_text='Enter Venue Title',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    prog_id = forms.ModelChoiceField(queryset=Programme.objects.all(), empty_label="(Select Programme Type)", required=True, help_text="Select Programme Type", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    class Meta:
        model = Venue
        fields = ('venue_title', 'prog_id')

class DefenseDaysForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.dept_id = kwargs.pop('dept_id', '')
        super(DefenseDaysForm, self).__init__(*args, **kwargs)

    num_of_day = forms.CharField(help_text='Enter Number of day',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    prog_id = forms.ModelChoiceField(queryset=Programme.objects.all(), empty_label="(Select Programme Type)", required=True, help_text="Select Programme Type", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    sess_id = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session Type)", required=True, help_text="Select Session Type", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))


    type_id = forms.ModelChoiceField(queryset=StudentType.objects.all(), empty_label="(Select Student Type)", required=True, help_text="Select Student Type", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    def clean(self):
        cleaned_data = super().clean()
        sess = cleaned_data.get('sess_id')
        prog_id = cleaned_data.get('prog_id')
        type_id = cleaned_data.get('type_id')

        check = DaysOfDefense.objects.filter(sess_id=sess, dept_id=self.dept_id, type_id=type_id, prog_id=prog_id)
        if self.instance:
            check = check.exclude(pk=self.instance.pk)
        if check.exists():
            raise ValidationError('Entry already exist try editing!')

    class Meta:
        model = DaysOfDefense
        fields = ('num_of_day', 'prog_id', 'sess_id', 'type_id')

class EditDefenseDaysForm(DefenseDaysForm):

    def clean(self):
        pass

class StudHallAllocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.dept_id = kwargs.pop('dept_id', '')
        super(StudHallAllocationForm, self).__init__(*args, **kwargs)

    sess_id = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session Type)", required=True, help_text="Select Session Type", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    prog_id = forms.ModelChoiceField(queryset=Programme.objects.all(), empty_label="(Select Programme)", required=True, help_text="Select Programme", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    type_id = forms.ModelChoiceField(queryset=StudentType.objects.all(), empty_label="(Select Student Type)", required=True, help_text="Select Student Type", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    def clean(self):
        cleaned_data = super().clean()
        sess = cleaned_data.get('sess_id')
        prog_id = cleaned_data.get('prog_id')
        type_id = cleaned_data.get('type_id')

        check = StudHallAllocation.objects.filter(sess_id=sess, dept_id=self.dept_id, type_id=type_id, prog_id=prog_id).exists()

        if check:
            raise ValidationError('Allocation record already exist try editing!')
    class Meta:
        model = StudHallAllocation
        fields = ('prog_id', 'sess_id', 'type_id')

class RStudHallAllocationForm(StudHallAllocationForm):
    stud_id = forms.ModelChoiceField(queryset=StudentProfile.objects.all(), empty_label="(Select Student)", required=True, help_text="Select Student", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))
    def clean(self):
        pass

class MStudHallAllocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.dept_id = kwargs.pop('dept_id', '')
        super(MStudHallAllocationForm, self).__init__(*args, **kwargs)
        self.fields['stud_id'].queryset=StudentProfile.objects.filter(dept_id=self.dept_id)

    day_num = forms.CharField(help_text='Enter 1 for Day One',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    stud_id = forms.ModelChoiceField(queryset=StudentProfile.objects.all(), empty_label="(Select Student Type)", required=True, help_text="Select Student Type", widget=forms.Select(
        attrs={
            'class':'form-control searchable',
        }
    ))

    venue_id = forms.ModelChoiceField(queryset=Venue.objects.all(), empty_label="(Select Defense Venue)", required=True, help_text="Select Defense Venue", widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))

    def clean(self):
        cleaned_data = super().clean()
        stud_id = cleaned_data.get('stud_id')

        check = StudHallAllocation.objects.filter(dept_id=self.dept_id, stud_id=stud_id).exists()

        if check:
            raise ValidationError('Allocation record already exist try editing!')

    class Meta:
        model = StudHallAllocation
        fields = ('day_num', 'stud_id', 'venue_id')


