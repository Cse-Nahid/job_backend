from django.db import models
from django.conf import settings

class Application(models.Model):
    job_seeker = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='applications'
    )
    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.CASCADE,
        related_name='applications'
    )
    resume = models.FileField(upload_to='resumes/')  # Ensure this field exists
    date_applied = models.DateField(auto_now_add=True)  # Ensure this field exists

    def __str__(self):
        return f"{self.job_seeker} applied for {self.job}"
