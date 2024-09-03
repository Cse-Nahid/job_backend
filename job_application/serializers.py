from rest_framework import serializers
from .models import JobApplication
from jobseeker.models import Jobseeker
from job_post.models import JobPost
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]


class JobSeekerSerializer(serializers.ModelSerializer):
    # to view the user account details too
    user = UserSerializer(read_only=True)

    class Meta:
        model = Jobseeker
        fields = '__all__'

        read_only_fields = ["user", ]


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'



class JobApplicationSerializer(serializers.ModelSerializer):
    # StringRelatedField for nested serializers, to only show the user name, not the whole job_seeker object data
    # job_seeker = serializers.StringRelatedField(many=False)
    # job_post = serializers.StringRelatedField(many=False)
    
    # to see the full detail of job_seeker
    job_seeker = JobSeekerSerializer(read_only=True)

    # to see the full detail of job_seeker
    job_post = JobPostSerializer(read_only=True)



    class Meta:
        model = JobApplication
        fields = '__all__'
        
        # # to automatically set the job_seeker based on the currently authenticated user.    # by making 'job_seeker' read_only, we dont need to provide it from the frontend 
        
        # also making "job_post" read-only for the same purpose
        read_only_fields = ["job_seeker", "job_post"]
