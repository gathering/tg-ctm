from django import forms
from .models import *

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description']

class TaskTimeSlotForm(forms.ModelForm):
    class Meta:
         model = TaskTimeSlot
         fields = ['starts', 'ends', 'task', 'max_participants']

class TaskTimeSlotUserForm(forms.ModelForm):
    class Meta:
        model = TaskTimeSlotUser
        fields = ["user", "timeslot"]

class CheckInUserTaskTimeSlotForm(forms.ModelForm):
    class Meta:
        model = CheckInUserTaskTimeSlot
        fields = ["user", "timeslot"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["wannabe_id"]

class CrewForm(forms.ModelForm):
    class Meta:
        model = Crew
        fields = ["name", "crew_id"]

class RegisterAttendanceForm(forms.Form):
    nfc_tag = forms.CharField(label='NFC Tag')
    