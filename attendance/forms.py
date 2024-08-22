from django import forms
from .models import Attendance
from django.conf import settings


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user', 'date', 'check_in_time', 'check_out_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class AttendanceSearchForm(forms.Form):
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    user = forms.ModelChoiceField(queryset=settings.AUTH_USER_MODEL.objects.all(), required=False)
