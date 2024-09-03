from django.contrib import admin
from .models import JobPost



# Register your models here.
class JobPostAdmin(admin.ModelAdmin):    
    def company(self, obj):
        return obj.employer.company_name
    
    def status(self, obj):
        return obj.employment_status
    
    list_display = ['id', 'job_title', 'company', 'status', 'education', 'experience', 'age', 'vacancy', 'salary', 'job_posted_on', 'deadline']



admin.site.register(JobPost, JobPostAdmin)