from django.db import models
from accounts.models import CustomUser



# Create your models here.
class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer')

    company_name = models.CharField(max_length=50)
    company_address = models.TextField()
    business_info = models.TextField()


    def __str__(self):
        return f'{self.company_name}'