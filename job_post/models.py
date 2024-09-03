from django.db import models

from employer.models import Employer
from job_catagory.models import Category

from django.core.validators import MinValueValidator




# Create your models here.
class JobPost(models.Model):
    job_title = models.CharField(max_length=100)

    job_category = models.ManyToManyField(Category, related_name='job_category')

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='employer')
    
    job_location = models.CharField(max_length=50)
    employment_status = models.CharField(max_length=20, choices=[('full-time', 'Full-time'), ('part-time', 'Part-time'), ('contractual', 'Contractual'), ('permanent', 'Permanent')])
    
    job_context = models.TextField()
    job_responsibilities = models.TextField()

    education = models.TextField()
    experience = models.TextField()
    age = models.IntegerField(validators=[MinValueValidator(18)])

    vacancy = models.IntegerField()
    salary = models.IntegerField()
    other_benefits = models.TextField(blank=True, null=True)

    job_posted_on = models.DateField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deadline = models.DateField()

    application_instructions = models.TextField()



    def __str__(self):
        return f'{self.job_title} at: {self.employer.company_name}'
    
