from django.contrib import admin
from .models import StudentDropout, Intervention

class StudentDropoutAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'area', 'get_gender_display', 'caste', 'age', 'standard', 'dropout_year')
    list_filter = ('school_name', 'area', 'gender', 'caste', 'standard', 'date_of_dropout')  # Changed here
    search_fields = ('school_name', 'area', 'caste')
    
    def get_gender_display(self, obj):
        return obj.get_gender_display()
    get_gender_display.short_description = 'Gender'

    def dropout_year(self, obj):
        return obj.date_of_dropout.year
    dropout_year.short_description = 'Dropout Year'

class InterventionAdmin(admin.ModelAdmin):
    list_display = ('title', 'intervention_type', 'school_name', 'area', 'start_date', 'end_date', 'status')
    list_filter = ('intervention_type', 'status', 'school_name', 'area')
    search_fields = ('title', 'description', 'school_name', 'area')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'intervention_type', 'status')
        }),
        ('Target Information', {
            'fields': ('school_name', 'area', 'target_gender', 'target_caste', 'target_standard')
        }),
        ('Timeline & Budget', {
            'fields': ('start_date', 'end_date', 'budget')
        }),
    )

admin.site.register(StudentDropout, StudentDropoutAdmin)
admin.site.register(Intervention, InterventionAdmin)
