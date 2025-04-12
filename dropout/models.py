from django.db import models
from django.utils import timezone

class StudentDropout(models.Model):
    school_name = models.CharField(max_length=255)
    area = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    caste = models.CharField(max_length=100)
    standard = models.CharField(max_length=10)
    age = models.IntegerField()
    date_of_dropout = models.DateField(default='2023-01-01')
    reason = models.TextField(default='Unknown')  # ✅ Added default here

    def __str__(self):
        return f"{self.school_name} - {self.standard} - {self.gender}"

class Intervention(models.Model):
    INTERVENTION_TYPES = [
        ('counseling', 'Counseling Program'),
        ('financial', 'Financial Support'),
        ('academic', 'Academic Support'),
        ('community', 'Community Outreach'),
        ('infrastructure', 'Infrastructure Improvement'),
        ('other', 'Other')
    ]

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    intervention_type = models.CharField(max_length=20, choices=INTERVENTION_TYPES)
    school_name = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    target_gender = models.CharField(max_length=1, blank=True, null=True)
    target_caste = models.CharField(max_length=100, blank=True, null=True)
    target_standard = models.CharField(max_length=10, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='planned')
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
  