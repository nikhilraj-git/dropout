from django.db import models

class StudentDropout(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    
    school_name = models.CharField(max_length=255)
    area = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    caste = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    standard = models.CharField(max_length=10)
    dropout_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.school_name} ({self.standard}) - {self.gender}"
