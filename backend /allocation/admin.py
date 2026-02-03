from django.contrib import admin
from .models import SupervisorProfile, StudentProposal

@admin.register(SupervisorProfile)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')

@admin.register(StudentProposal)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)