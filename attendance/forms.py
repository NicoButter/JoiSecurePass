from django import forms
from .models import Attendance
from accounts.models import CustomUser  


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user', 'date', 'check_in_time', 'check_out_time'] 

class AttendanceSearchForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=False)
    date = forms.DateField(required=False)
