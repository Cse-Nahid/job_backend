from django.contrib import admin
from .models import JobApplication

# Register your models here.
class JobApplicationAdmin(admin.ModelAdmin):
    def first_name(self, obj):
        return obj.job_seeker.user.first_name
    
    def last_name(self, obj):
        return obj.job_seeker.user.last_name
    
    def position(self, obj):
        return obj.job_post.job_title
    
    def employer(self, obj):
        return obj.job_post.employer
    
    def deadline(self, obj):
        return obj.job_post.deadline
    
    list_display = ['id', 'first_name', 'last_name', 'position', 'employer', 'applied_on', 'deadline', 'salary', 'resume']


admin.site.register(JobApplication, JobApplicationAdmin)