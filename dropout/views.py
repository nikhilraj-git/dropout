from django.shortcuts import render
from .models import StudentDropout
from django.db.models import Count

def dashboard(request):
    context = {
        'school_wise': StudentDropout.objects.values('school_name').annotate(count=Count('id')),
        'area_wise': StudentDropout.objects.values('area').annotate(count=Count('id')),
        'gender_wise': StudentDropout.objects.values('gender').annotate(count=Count('id')),
        'caste_wise': StudentDropout.objects.values('caste').annotate(count=Count('id')),
        'standard_wise': StudentDropout.objects.values('standard').annotate(count=Count('id')),
    }
    return render(request, 'dropout/dashboard.html', context)
