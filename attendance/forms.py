from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'check_in_time', 'check_out_time']

class AttendanceSearchForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
