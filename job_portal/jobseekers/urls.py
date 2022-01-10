from django.urls import path
from jobseekers import views

urlpatterns=[
    path("home",views.Jobseekerhome.as_view(),name="jobseekerhome"),
    path("jobs/profile/add",views.AddJobseekerProfile.as_view(),name="addjobseekeerprofile"),
    path("jobs/profile/change/<int:id>",views.ChangeJobseekerProfile.as_view(),name="changejpbseekerprofile"),
    path("jobs/view",views.ViewJobs.as_view(),name="viewjobs"),
    path("jobs/apply/<int:id>",views.ApplyJobss.as_view(),name="applyjob"),
    path("jobs/applied/view",views.AppliedJobs.as_view(),name="appliedjobs"),
    path("jobs/applications/remove/<int:id>",views.RemoveJobApplication.as_view(),name="removejobapplication"),
    path("jobs/applications/selected",views.SelectedJobs.as_view(),name="selected"),
    path("jobs/applications/interviewed",views.InterviewedJobs.as_view(),name="interview")
]