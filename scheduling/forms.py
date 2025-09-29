from django import forms
from django.forms import modelformset_factory
from .models import Employee, Location, Holiday, EmployeeOffDay
from datetime import date, datetime
import calendar


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'gender', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'mall_name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mall_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['name', 'date', 'is_recurring']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class OffDayForm(forms.ModelForm):
    class Meta:
        model = EmployeeOffDay
        fields = ['employee', 'date', 'reason']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ScheduleGenerationForm(forms.Form):
    MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
    YEAR_CHOICES = [(i, i) for i in range(date.today().year, date.today().year + 3)]

    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=date.today().month
    )
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=date.today().year
    )
    locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )


# Create formsets for bulk operations
EmployeeFormSet = modelformset_factory(Employee, form=EmployeeForm, extra=3, can_delete=True)
LocationFormSet = modelformset_factory(Location, form=LocationForm, extra=2, can_delete=True)