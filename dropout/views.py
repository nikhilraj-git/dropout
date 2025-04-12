from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator
import csv
from .models import StudentDropout

def dashboard(request):
    # Get filter parameters
    selected_school = request.GET.get('school', '')
    selected_area = request.GET.get('area', '')
    selected_year = request.GET.get('year', '')
    
    # Base queryset
    queryset = StudentDropout.objects.all()
    
    # Apply filters if provided
    if selected_school:
        queryset = queryset.filter(school_name=selected_school)
    if selected_area:
        queryset = queryset.filter(area=selected_area)
    if selected_year:
        queryset = queryset.filter(dropout_year=selected_year)
    
    # Get all dropouts for table view with pagination
    paginator = Paginator(queryset.order_by('-date_of_dropout', 'school_name'), 10)
  # Show 10 records per page
    page_number = request.GET.get('page')
    dropouts = paginator.get_page(page_number)
    
    # Get aggregated data for charts
    school_wise = list(queryset.values('school_name').annotate(count=Count('id')).order_by('-count'))
    area_wise = list(queryset.values('area').annotate(count=Count('id')).order_by('-count'))
    gender_wise = list(queryset.values('gender').annotate(count=Count('id')))
    caste_wise = list(queryset.values('caste').annotate(count=Count('id')).order_by('-count'))
    standard_wise = list(queryset.values('standard').annotate(count=Count('id')))
    year_wise = list(queryset.values('dropout_year').annotate(count=Count('id')).order_by('dropout_year'))
    
    # Additional charts for trends tab
    age_distribution = list(queryset.values('age').annotate(count=Count('id')).order_by('age'))
    
    # Area-Gender distribution
    area_gender_distribution = list(queryset.values('area', 'gender').annotate(count=Count('id')).order_by('area', 'gender'))
    
    # Age-Standard distribution
    age_standard_distribution = list(queryset.values('age', 'standard').annotate(count=Count('id')))
    
    # For filter dropdowns
    schools = StudentDropout.objects.values('school_name').distinct()
    areas = StudentDropout.objects.values('area').distinct()
    years = StudentDropout.objects.values('dropout_year').distinct().order_by('-dropout_year')
    
    # Summary statistics
    total_dropouts = queryset.count()
    school_count = queryset.values('school_name').distinct().count()
    
    # Find high risk area (area with highest dropout rate)
    high_risk_area = area_wise[0]['area'] if area_wise else "None"
    
    # Latest year analyzed
    latest_year = StudentDropout.objects.order_by('-dropout_year').values_list('dropout_year', flat=True).first() or 0
    
    context = {
        'dropouts': dropouts,
        'school_wise': school_wise,
        'area_wise': area_wise,
        'gender_wise': gender_wise,
        'caste_wise': caste_wise,
        'standard_wise': standard_wise,
        'year_wise': [{'year': item['dropout_year'], 'count': item['count']} for item in year_wise],
        'age_distribution': age_distribution,
        'area_gender_distribution': area_gender_distribution,
        'age_standard_distribution': age_standard_distribution,
        'total_dropouts': total_dropouts,
        'school_count': school_count,
        'high_risk_area': high_risk_area,
        'latest_year': latest_year,
        'schools': schools,
        'areas': areas,
        'years': years,
        'selected_school': selected_school,
        'selected_area': selected_area,
        'selected_year': selected_year,
    }
    
    return render(request, 'dropout/dashboard.html', context)

def export_csv(request):
    # Get filter parameters
    selected_school = request.GET.get('school', '')
    selected_area = request.GET.get('area', '')
    selected_year = request.GET.get('year', '')
    
    # Base queryset
    queryset = StudentDropout.objects.all()
    
    # Apply filters if provided
    if selected_school:
        queryset = queryset.filter(school_name=selected_school)
    if selected_area:
        queryset = queryset.filter(area=selected_area)
    if selected_year:
        queryset = queryset.filter(dropout_year=selected_year)
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dropout_data.csv"'
    
    # Write to CSV
    writer = csv.writer(response)
    writer.writerow(['School Name', 'Area', 'Gender', 'Caste', 'Age', 'Standard', 'Dropout Year'])
    
    for dropout in queryset:
        gender_display = {
            'M': 'Male',
            'F': 'Female',
            'O': 'Other'
        }.get(dropout.gender, dropout.gender)
        
        writer.writerow([
            dropout.school_name,
            dropout.area,
            gender_display,
            dropout.caste,
            dropout.age,
            dropout.standard,
            dropout.dropout_year
        ])
    
    return response