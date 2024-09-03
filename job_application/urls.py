from django.urls import path, include

from .views import JobApplicationListView, JobApplicationApplyView, JobApplicationDetailView, JobApplicationForAJobSeekerAPIView, JobApplicationsForJobPostAPIView, CheckJobApplicationView



urlpatterns = [
    path("all/", JobApplicationListView.as_view(), name="application_list"),
    path("all/<int:pk>/", JobApplicationDetailView.as_view(), name="application_detail"),

    path("apply/", JobApplicationApplyView.as_view(), name="apply_application"),

    path('my_applications/', JobApplicationForAJobSeekerAPIView.as_view(), name='my_applications'),
    path('check_application/', CheckJobApplicationView.as_view(), name='check_application'),

    path('applications_for_a_job_post/', JobApplicationsForJobPostAPIView.as_view(), name='applications_for_a_job_post'),
]