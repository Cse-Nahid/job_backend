from django.urls import path, include
from .views import JobPostListView, JobPostPublishView, JobPostDetailView, JobPostForAnEmployerAPIView, JobPostsOfJobCategoryAPIView

from . import views

urlpatterns = [
    # path('', views.job_post_views, name='job_post_list'),
    path("all/", JobPostListView.as_view(), name="post_list"),
    path("all/<int:pk>/", JobPostDetailView.as_view(), name="post_detail"),

    path("publish/", JobPostPublishView.as_view(), name="publish_post"),

    path('my_advertisements/', JobPostForAnEmployerAPIView.as_view(), name='my_advertisements'),

    path('job_posts_of_a_category/', JobPostsOfJobCategoryAPIView.as_view(), name='job_posts_of_a_category'),
]


