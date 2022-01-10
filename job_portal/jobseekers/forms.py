from django import forms
from django.forms import ModelForm

from employer import models

class JobseekerProfileForm(ModelForm):
    class Meta:
        model=models.JobSeekerProfile
        fields=["name","profile_pic","qualification","experience","resume"]

        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "qualification":forms.TextInput(attrs={"class":"form-control"}),
            "experience":forms.NumberInput(attrs={"class":"form-control"}),
        }

class JobApplication(ModelForm):
    class Meta:
        model=models.Application
        fields=["job"]

    widgets={
        "job":forms.TextInput(attrs={'readonly':'readonly'})
    }

