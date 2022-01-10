from itertools import count

from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator

from employer import decorators
from employer.decorators import Sign_required

from employer.forms import CompanyProfileForm
from employer.models import MyUser, CompanyProfile, Jobs, Application, JobSeekerProfile
from django.forms import forms
from employer import forms
from django.urls import reverse_lazy
# Create your views here.
from django.views.generic import CreateView,ListView,TemplateView,DetailView,UpdateView,DeleteView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import wget

class UserRegistrationView(CreateView):
    model = MyUser
    form_class = forms.UserRegistrationForm
    template_name = 'employer/signup.html'
    success_url = reverse_lazy("signin")

    # def post(self, request, *args, **kwargs):
    #     form=self.form_class(request.post)
    #     if form.is_valid():
    #         form.save()

class SigninView(TemplateView):
    template_name = 'employer/signin.html'
    form_class=forms.SigninForm

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["form"]=self.form_class()
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            print(email,password)
            print(user)
            if user:
                login(request, user)
                print(user.role)
                if request.user.role=='employer':
                    return redirect("employerhome")
                elif user.role=='job_seeker':
                    return redirect("jobseekerhome")
                    print("failed")
            else:
                messages.error(request, "please enter correct username/password")
                return redirect('signin')

class SignOutView(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("signin")

@method_decorator(Sign_required,name='dispatch')
class EmployerHomeView(TemplateView):
    template_name = 'employer/employerhome.html'

@method_decorator(Sign_required,name='dispatch')
class CompanyProfileView(TemplateView):
    model=CompanyProfile
    template_name = "employer/addcompanyprofile.html"
    form_class=forms.CompanyProfileForm

    # def get_query_set(self,request,*args,**kwargs):
    #     return CompanyProfile.objects.filter(company=request.user)

    def get(self, request, *args, **kwargs):
        form=self.form_class

        company_data = self.model.objects.filter(company=request.user)
        return render(request, self.template_name, {"form":form,"profile": company_data})
    #
    # def get_context_data(self, **kwargs):
    #     # query=self.get_query_set()
    #     context=super().get_context_data(**kwargs)
    #     context["form"]=self.form_class
    #     return context
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            # form.save()
            jobs=form.save(commit=False)
            jobs.company=request.user
            data=self.model.objects.filter(company=jobs.company)

            if data:
                print("already added")
                messages.error(request,"company profile already added")
                return redirect("addcompanyprofile")
            else:
                jobs.save()
                return redirect("employerhome")


        else:
            print("failed")
            return render(request,self.template_name,{"form":form})

@method_decorator(Sign_required,name='dispatch')
class CompanyProfileEditView(UpdateView):
    model = CompanyProfile
    form_class = forms.CompanyEditProfileForm
    template_name = "employer/edit_companyprofile.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy('employerhome')

@method_decorator(Sign_required,name='dispatch')
class JobAddView(CreateView):
    model = Jobs
    form_class = forms.AddingJobsForm
    template_name = "employer/addjobs.html"
    success_url = reverse_lazy("addjobs")

    def post(self, request, *args, **kwargs):

        company=CompanyProfile.objects.get(company=request.user)
        print("coommppp",company)
        form = self.form_class(request.POST)
        if form.is_valid():
            jobs=form.save(commit=False)
            jobs.company=company
            jobs.save()
            return redirect("addjobs")
        else:
            return redirect("employerhome")

@method_decorator(Sign_required,name='dispatch')
class JobsView(TemplateView):
    model=Jobs
    template_name = "employer/jobsview.html"
    form_class=forms.AddingJobsForm
    queryset=model.objects.all()

    # def get(self, request, *args, **kwargs):
    #     form=self.form_class(request.user)
    #     company_profile=CompanyProfile.objects.filter(company=request.user)
    #     print("company",company_profile)
    #     profile_id=company_profile.id
    #     print("profile_id",profile_id)
    #     jobs=self.model.objects.filter(company_id=profile_id)
    #     print("jobs",jobs)
    #     return render(request,self.template_name,{"form":form,"jobs":jobs})


    def get(self, request, *args, **kwargs):
        try:
            company_profile = CompanyProfile.objects.get(company=request.user)
            print("profile", company_profile)
            print("profile", company_profile.id)
            profile_id = company_profile.id
            jobs = Jobs.objects.filter(company_id=profile_id)
            print("forms", jobs)
            return render(request, self.template_name, {"form": jobs})
        except Exception as e:
            messages.error(request, "you didn't add any jobs yet")
            return render(request, self.template_name)

@method_decorator(Sign_required,name='dispatch')
class ChangeJobsView(UpdateView):
    model = Jobs
    template_name = "employer/edit_jobs.html"
    form_class = forms.AddingJobsForm
    pk_url_kwarg = "id"
    success_url = reverse_lazy("jobsview")

@method_decorator(Sign_required,name='dispatch')
class RemoveJobs(DeleteView):
    model = Jobs
    template_name = "employer/removejobs.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("jobsview")

@method_decorator(Sign_required,name='dispatch')
class ApplicationView(TemplateView):
    model= Application
    template_name = "employer/applicationview.html"
    queryset=model.objects.all()


    def get(self,request,*args,**kwargs):
        global a
        user=CompanyProfile.objects.get(company=request.user)
        profile_id=user.id
        print(profile_id)
        application=Application.objects.filter(company_id=profile_id,application_status="applied")

        print("sdsdsf",application)
        return render(request,self.template_name,{"form":application})



@method_decorator(Sign_required,name='dispatch')
class JobApplied(TemplateView):
    model = Application
    pk_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        application = self.model.objects.get(id=kwargs["id"])
        application.application_status = "intouch"
        application.save()
        return redirect("jobsview")


@method_decorator(Sign_required,name='dispatch')
class InterViewSelectedView(TemplateView):
    model = Application
    template_name = "employer/interview_view.html"
    queryset = model.objects.all()

    def get(self,request,*args,**kwargs):
        user = CompanyProfile.objects.get(company=request.user)
        profile_id = user.id
        print(profile_id)
        application = Application.objects.filter(company_id=profile_id, application_status="intouch")

        print("sdsdsf", application)
        return render(request, self.template_name, {"form": application})


@method_decorator(Sign_required,name='dispatch')
class SelectedJobs(TemplateView):
    model = Application
    pk_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        application = self.model.objects.get(id=kwargs["id"])
        application.application_status = "selected"
        application.save()
        return redirect("jobsview")

@method_decorator(Sign_required,name='dispatch')
class NotSelected(TemplateView):
    model = Application
    pk_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        application = self.model.objects.get(id=kwargs["id"])
        application.application_status = "not selected"
        application.save()
        return redirect("jobsview")


class ProfileView(TemplateView):
    model= JobSeekerProfile
    template_name = "employer/userprofile.html"
    pk_url_kwarg = "id"

    def get(self,request,*args,**kwargs):
        user=self.model.objects.get(user_id=kwargs["id"])
        print("okfdofodsjf",user.experience)



        # print('Beginning file download with wget module')
        #
        # url = user.resume
        # wget.download(url)



        return render(request, self.template_name, {"user": user})


@method_decorator(Sign_required,name='dispatch')
class SelectedParticipantView(TemplateView):
    model = Application
    template_name = "employer/paricipantselectedview.html"
    queryset = model.objects.all()

    def get(self,request,*args,**kwargs):
        user = CompanyProfile.objects.get(company=request.user)
        profile_id = user.id
        print(profile_id)
        application = Application.objects.filter(company_id=profile_id, application_status="selected")

        print("sdsdsf", application)
        return render(request, self.template_name, {"form": application})


