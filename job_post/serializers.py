from rest_framework import serializers
from .models import JobPost
from employer.models import Employer



class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['company_name', 'company_address', 'business_info', ]



class JobPostSerializer(serializers.ModelSerializer):
    # StringRelatedField for nested serializers, to only show the user name, not the whole employer object data
    # employer = serializers.StringRelatedField(many=False)

    # to see the full details of employer
    employer = EmployerSerializer(read_only=True)
    
    # job_category = serializers.StringRelatedField(many=True)


    class Meta:
        model = JobPost
        fields = '__all__'
        
        # to automatically set the employer based on the currently authenticated user.      # by making 'employer' read_only, we dont need to provide it from the frontend form
        read_only_fields = ["employer",]
        
