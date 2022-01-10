from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from employer.models import MyUser,CompanyProfile,Jobs


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = MyUser
        fields = ["email","phone", "role", "password1", "password2"]
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "phone":forms.NumberInput(attrs={"class":"form-control"}),
            "role": forms.Select(attrs={"class": "form-select"})
        }

    def __str__(self):
        return self.email

class SigninForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class CompanyProfileForm(ModelForm):
    company=UserRegistrationForm()
    class Meta:
        model=CompanyProfile
        fields=["company_name","description","logo"]

        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-textarea"}),
        }

    def clean(self):
        cleaned_data=super().clean()
        company_name=cleaned_data["company_name"]
        print("company name",company_name)
        company=CompanyProfile.objects.filter(company_name__iexact=company_name)
        print("coooommpp",company)
        if company:
            msg="The company name is already exist"
            self.add_error("company_name",msg)



class CompanyEditProfileForm(ModelForm):
    company=UserRegistrationForm()
    class Meta:
        model=CompanyProfile
        fields=["id","company_name","description","logo"]

        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-textarea"}),
        }

    def clean(self):
        cleaned_data=super().clean()
        company_name=cleaned_data["company_name"]
        print("company name",company_name)
        company=CompanyProfile.objects.filter(company_name__iexact=company_name)
        print("coooommpp",company)
        if company:
            msg="The company name is already exist"
            self.add_error("company_name",msg)

class AddingJobsForm(ModelForm):

    class Meta:
        model = Jobs
        fields = ["id","post_name", "experience", "description"]
        widgets = {
            "post_name": forms.TextInput(attrs={"class": "form-control"}),
            "experience": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"})
        }


