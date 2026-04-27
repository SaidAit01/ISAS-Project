from django.contrib import admin
from .models import StudentProposal, SupervisorProfile, SystemConfiguration, ProjectCategory, TechnicalSkill, ResearchInterest


admin.site.register(SystemConfiguration)
admin.site.register(ProjectCategory)
admin.site.register(TechnicalSkill)
admin.site.register(ResearchInterest)

@admin.register(SupervisorProfile)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')

@admin.register(StudentProposal)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)


