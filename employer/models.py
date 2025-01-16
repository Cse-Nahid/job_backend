from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    business_info = models.TextField()
    company_description = models.TextField()
    first_name = models.CharField(max_length=255, default='Default Name')
    last_name = models.CharField(max_length=255, default='Default Last Name')  # Add a default for last_name as well

    def __str__(self):
        return self.company_name
