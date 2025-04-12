from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models.functions import ExtractYear
from dropout.models import StudentDropout
import json
from pathlib import Path

class Command(BaseCommand):
    help = 'Generate insights from dropout data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating insights...'))
        
        insights = {
            'high_risk_schools': self._get_high_risk_schools(),
            'age_patterns': self._get_age_patterns(),
            'gender_disparities': self._get_gender_disparities(),
            'area_analysis': self._get_area_analysis(),
            'year_trends': self._get_year_trends(),
            'caste_correlations': self._get_caste_correlations(),
        }
        
        # Save insights to a JSON file
        output_file = Path('dropout_insights.json')
        with open(output_file, 'w') as f:
            json.dump(insights, f, indent=4)
        
        self.stdout.write(self.style.SUCCESS(f'Insights generated and saved to {output_file}'))
    
    def _get_high_risk_schools(self):
        """Identify schools with the highest dropout rates"""
        schools = StudentDropout.objects.values('school_name') \
            .annotate(count=Count('id')) \
            .order_by('-count')[:3]
        
        # For each high-risk school, get additional details
        results = []
        for school in schools:
            school_queryset = StudentDropout.objects.filter(school_name=school['school_name'])
            
            # Get most common dropout reasons by grade
            standard_breakdown = school_queryset.values('standard') \
                .annotate(count=Count('id')) \
                .order_by('-count')[:3]
            
            # Get gender breakdown
            gender_breakdown = school_queryset.values('gender') \
                .annotate(count=Count('id'))
            
            # Format gender display names
            gender_display = {}
            for item in gender_breakdown:
                if item['gender'] == 'M':
                    gender_display['Male'] = item['count']
                elif item['gender'] == 'F':
                    gender_display['Female'] = item['count']
                else:
                    gender_display['Other'] = item['count']
            
            results.append({
                'school_name': school['school_name'],
                'total_dropouts': school['count'],
                'standard_breakdown': list(standard_breakdown),
                'gender_breakdown': gender_display
            })
        
        return results
    
    def _get_age_patterns(self):
        """Analyze age patterns in dropouts"""
        # Overall age distribution
        age_distribution = StudentDropout.objects.values('age') \
            .annotate(count=Count('id')) \
            .order_by('age')
        
        # Find critical age with highest dropout rate
        critical_age = StudentDropout.objects.values('age') \
            .annotate(count=Count('id')) \
            .order_by('-count')[:1]
        
        # Age vs. standard correlation
        age_standard = StudentDropout.objects.values('age', 'standard') \
            .annotate(count=Count('id')) \
            .order_by('-count')[:10]
        
        return {
            'age_distribution': list(age_distribution),
            'critical_age': list(critical_age),
            'age_standard_correlation': list(age_standard)
        }
    
    def _get_gender_disparities(self):
        """Analyze gender disparities in dropouts"""
        # Overall gender distribution
        gender_distribution = StudentDropout.objects.values('gender') \
            .annotate(count=Count('id'))
        
        # Format gender display names
        gender_display = []
        for item in gender_distribution:
            if item['gender'] == 'M':
                gender_display.append({'gender': 'Male', 'count': item['count']})
            elif item['gender'] == 'F':
                gender_display.append({'gender': 'Female', 'count': item['count']})
            else:
                gender_display.append({'gender': 'Other', 'count': item['count']})
        
        # Gender distribution by area
        gender_area = StudentDropout.objects.values('gender', 'area') \
            .annotate(count=Count('id')) \
            .order_by('area', '-count')
        
        # Format for gender area display
        gender_area_display = []
        for item in gender_area:
            gender_name = 'Male' if item['gender'] == 'M' else 'Female' if item['gender'] == 'F' else 'Other'
            gender_area_display.append({
                'gender': gender_name,
                'area': item['area'],
                'count': item['count']
            })
        
        return {
            'gender_distribution': gender_display,
            'gender_area_distribution': gender_area_display
        }
    
    def _get_area_analysis(self):
        """Analyze area-based patterns in dropouts"""
        # Overall area distribution
        area_distribution = StudentDropout.objects.values('area') \
            .annotate(count=Count('id')) \
            .order_by('-count')
        
        # Area vs. caste analysis
        area_caste = StudentDropout.objects.values('area', 'caste') \
            .annotate(count=Count('id')) \
            .order_by('area', '-count')
        
        return {
            'area_distribution': list(area_distribution),
            'area_caste_analysis': list(area_caste)
        }
    
    

    def _get_year_trends(self):
        """Analyze dropout trends over the years."""

        # Yearly dropout trends
        year_trends = (
            StudentDropout.objects
            .annotate(dropout_year=ExtractYear('date_of_dropout'))
            .values('dropout_year')
            .annotate(total=Count('id'))
            .order_by('dropout_year')
        )

        # Dropouts per year per school
        year_school_analysis = (
            StudentDropout.objects
            .annotate(dropout_year=ExtractYear('date_of_dropout'))
            .values('dropout_year', 'school_name')
            .annotate(count=Count('id'))
            .order_by('dropout_year', '-count')
        )

        return {
            'yearly_trends': list(year_trends),
            'year_school_analysis': list(year_school_analysis),
        }



    
    def _get_caste_correlations(self):
        """Analyze caste-based patterns in dropouts"""
        # Overall caste distribution
        caste_distribution = StudentDropout.objects.values('caste') \
            .annotate(count=Count('id')) \
            .order_by('-count')
        
        # Caste distribution by school
        caste_school = StudentDropout.objects.values('caste', 'school_name') \
            .annotate(count=Count('id')) \
            .order_by('caste', '-count')
        
        return {
            'caste_distribution': list(caste_distribution),
            'caste_school_analysis': list(caste_school)
        }
