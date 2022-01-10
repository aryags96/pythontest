from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator

from employer.models import MyUser,JobSeekerProfile,Jobs,Application,CompanyProfile
from django.forms import forms
from jobseekers import forms
from django.urls import reverse_lazy
from employer.decorators import Sign_required
# Create your views here.
from django.contrib import messages
from datetime import timedelta,date
from django.views.generic import CreateView,ListView,TemplateView,DetailView,UpdateView,DeleteView

@method_decorator(Sign_required,name='dispatch')
class Jobseekerhome(TemplateView):
    template_name = 'jobseeker/jobseekerhome.html'

@method_decorator(Sign_required,name='dispatch')
class AddJobseekerProfile(CreateView):
    model=JobSeekerProfile
    template_name = "jobseeker/jobseekerprofile.html"
    form_class = forms.JobseekerProfileForm

    def get(self, request, *args, **kwargs):
        form=self.form_class
        jobseeker=self.model.objects.filter(user=request.user)
        print("jobseeker",jobseeker)
        return render(request,self.template_name,{"form":form,"profile":jobseeker})

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST,request.FILES)
        if form.is_valid():
            jobseeker=form.save(commit=False)
            jobseeker.user=request.user
            user=self.model.objects.filter(user=request.user)
            if user:
                print("added")
                messages.error(request,"user profile already added")
                return redirect("addjobseekeerprofile")
            else:
                jobseeker.save()
                return redirect("jobseekerhome")
        else:
            return render(request,self.template_name,{"form":form})


@method_decorator(Sign_required,name='dispatch')
class ChangeJobseekerProfile(UpdateView):
    model = JobSeekerProfile
    template_name = "jobseeker/jobseekerchangeprofile.html"
    form_class = forms.JobseekerProfileForm
    pk_url_kwarg = "id"
    success_url = reverse_lazy("addjobseekeerprofile")

@method_decorator(Sign_required,name='dispatch')
class ViewJobs(ListView):
    model=Jobs
    template_name = "jobseeker/jobviews.html"
    context_object_name = "jobs"

    # def get(self, request, *args, **kwargs):
    #     edd = date.today()
    #     print(edd)
    #     dates = self.model.objects.values_list('last_date')
    #     print("datesss", dates)
    #     # return redirect("viewjobs")
    #     if dates == edd:
    #         messages.error(request, "CLOSED")
    #         print("closed")
    #         return redirect("viewjobs")
    #     else:
    #         print("open")
    #         return redirect('viewjobs')










        # dates=self.model.objects.get(last_date)





#
# def applyJob(request,id,*args,**kwargs):
#     job = Jobs.objects.get(id=id)
#     job_ids = job.id
#     form = forms.JobApplication(initial={"job_id":job_ids})
#     context={"form":form,"job_id":job_ids}
#     print("id",job_ids)
#     if request.method == "POST":
#         form = forms.JobApplication(request.POST)
#         if form.is_valid():
#             data=form.cleaned_data["job_ids"]
#             print(data)
#             applications=form.save(commit=False)
#             applications.job=job_ids
#             applications.user=request.user
#             print(applications.user)
#             print(applications.job)
#             print("hai")
#             applications.save()
#             return redirect("jobseekerhome")
#         else:
#             return render("applyjob")
#
#
#     return render(request, 'jobseeker/jobviews.html', context)

@method_decorator(Sign_required,name='dispatch')
class ApplyJobss(CreateView):
    model = Jobs
    form_class = forms.JobApplication
    template_name = "jobseeker/jobapply.html"
    context_object_name = "jobs"
    pk_url_kwarg = "id"
    global fil

    def get(self, request, *args, **kwargs):
        job = Jobs.objects.get(id=kwargs["id"])
        job_ids=job.id
        fil = Application.objects.filter(user=request.user, job=job)

        print("idds",job_ids)

        form=self.form_class(initial={"job":job})
        # print("hi")
        return render(request,self.template_name,{"form":form})

    def post(self,request,*args,**kwargs):
        global fil
        form=self.form_class(request.POST)
        if form.is_valid():
            job=form.cleaned_data["job"]
            print("jobsd",job)
            data=form.save(commit=False)
            print("datadsdssss",data.job_id)
            jobid=data.job_id
            comp=Jobs.objects.get(id=jobid)

            ids=comp.company_id
            print("companuyidsssss",ids )
            compro=CompanyProfile.objects.get(id=ids)
            print("loop", compro)
            profileid=compro.id
            print("profileid",profileid)
            data.user=request.user
            data.company_id=profileid
            print("companyids",data.company_id)
            fil = Application.objects.filter(user=request.user, job=jobid)

            if fil:
                messages.error(request,"you have been already applied")
                print("hai")
                return redirect("viewjobs")
            else:
                data.save()
                print("jaifdsfs")
                return redirect("viewjobs")

        else:
            return render(request,self.template_name,{"form":form})


@method_decorator(Sign_required,name='dispatch')
class AppliedJobs(TemplateView):
    model = Application
    form_class=forms.JobApplication
    template_name = "jobseeker/appliedjobs.html"
    context_object_name = "jobs"
    queryset = model.objects.all()

    def get(self,request,*args,**kwargs):
        user_jobs = Application.objects.filter(user=request.user,application_status="applied")
        print(user_jobs)
        return render(request, self.template_name, {"company":user_jobs})

class SelectedJobs(TemplateView):
    model=Application
    form_class=forms.JobApplication
    template_name = "jobseeker/selectedjobs.html"
    queryset=model.objects.all()

    def get(self, request, *args, **kwargs):
        user_jobs= Application.objects.filter(user=request.user,application_status="selected")
        print(user_jobs)
        return render(request, self.template_name, {"company": user_jobs})


class InterviewedJobs(TemplateView):

        model = Application
        form_class = forms.JobApplication
        template_name = "jobseeker/interviewjobs.html"
        queryset = model.objects.all()

        def get(self, request, *args, **kwargs):
            user_jobs = Application.objects.filter(user=request.user, application_status="intouch")
            print(user_jobs)
            return render(request, self.template_name, {"company": user_jobs})



        # print("sdfdsfsdfsdfds",a)
        # jobs = Jobs.objects.filter(id=user_jobs.job_id)
        # print(jobs)
        # companyid=jobs.company_id
        # company=CompanyProfile.objects.get(id=companyid)
        # print("company",company)

        # print("job",jobs.id,"companyname",jobs.company_id,"postname",jobs.post_name)
        # print("application", user_jobs.job_id)
        # return render(request, self.template_name, {"form": jobs})

        # try:
        #     user=JobSeekerProfile.objects.get(id=request.user)
        #     print(user)
        #     user_jobs = self.model.objects.filter(user=request.user)
        #
        #     jobid = user_jobs.job_id
        #     # print("sdfdsfsdfsdfds",a)
        #     jobs = Jobs.objects.filter(id=jobid)
        #     # companyid=jobs.company_id
        #     # company=CompanyProfile.objects.get(id=companyid)
        #     # print("company",company)
        #
        #     # print("job",jobs.id,"companyname",jobs.company_id,"postname",jobs.post_name)
        #     print("application", user_jobs.job_id)
        #     return render(request, self.template_name, {"form": jobs})


        # except Exception as e:
        #     # print("abcccccccc")
        #     messages.error(request,"you didn't apply any jobs yet")
        #     return render(request, self.template_name)

@method_decorator(Sign_required,name='dispatch')
class RemoveJobApplication(DeleteView):
    model = Application
    template_name = "jobseeker/remove_job_application.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("addjobseekeerprofile")

# class ApplyJobs(CreateView):
#     model=Jobs
#     form_class = forms.JobApplication
#     template_name = "jobseeker/jobapply.html"
#     # pk_url_kwarg = "id"
#     success_url = reverse_lazy("viewjobs")
#
#     # def get(self, request, *args, **kwargs):
#     #     job = Jobs.objects.get(id=kwargs["id"])
#     #     print("jobs", job)
#     #     return redirect("addjobseekeerprofile")
#
#     def post(self,request,*args,**kwargs):
#         form=self.form_class(request.POST)
#         print(form)
#         print("haiiiiiiiiii")
#         print(request.user)
#
#         if form.is_valid():
#             jobs=form.save(commit=False)
#             jobs.user=request.user
#             form.save()
#             print("succcess")
#             return redirect("viewjobs")
#         else:
#             print("failed")
#             return redirect("viewjobs")






