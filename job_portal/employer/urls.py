from django.urls import path
from employer import views

urlpatterns=[
    path("jobs/accounts/signup",views.UserRegistrationView.as_view(),name="signup"),
    path("jobs/accounts/signin",views.SigninView.as_view(),name="signin"),
    path("jobs/employer/home",views.EmployerHomeView.as_view(),name="employerhome"),
    path("jobs/signout",views.SignOutView.as_view(),name="Signout"),
    path("jobs/company/add/profile",views.CompanyProfileView.as_view(),name="addcompanyprofile"),
    path("jobs/company/profile/change/<int:id>",views.CompanyProfileEditView.as_view(),name="editcompanyprofile"),
    path("jobs/add",views.JobAddView.as_view(),name="addjobs"),
    path("jobs/view",views.JobsView.as_view(),name="jobsview"),
    path("jobs/change/<int:id>",views.ChangeJobsView.as_view(),name="jobchange"),
    path("jobs/remove/<int:id>",views.RemoveJobs.as_view(),name="removejobs"),
    path("jobs/applications/view",views.ApplicationView.as_view(),name="empapplicationsview"),
    path("jobs/applications/reviewed/<int:id>",views.JobApplied.as_view(),name="reviewedjobs"),
    path("jobs/applications/reviewed/interview",views.InterViewSelectedView.as_view(),name="interview"),
    path("jobs/applications/jobs/selected/<int:id>",views.SelectedJobs.as_view(),name="selected"),
    path("jobs/applications/jobs/notselected/<int:id>",views.SelectedJobs.as_view(),name="notselected"),
    path("jobs/application/jobs/user/profile/<int:id>",views.ProfileView.as_view(),name="profile"),
    path("jobs/applications/reviewed/selected", views.SelectedParticipantView.as_view(), name="selectedparticipant"),

]