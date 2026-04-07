from django.db import models


# models containd the essentisl fields and behaviour of the data
class SupervisorProfile(models.Model) : 
    name = models.CharField(max_length=100)
    research_interests = models.JSONField(default=list) 
    suggested_projects = models.JSONField(default=list)
    required_skills = models.JSONField(default=list)
    project_categories = models.JSONField(default=list)
    capacity = models.IntegerField(default=5)

    def __str__(self):
        return self.name

class StudentProposal(models.Model):
    name = models.CharField(max_length=100)
    topic_description = models.TextField()
    student_research_interests = models.JSONField(default=list)
    technical_Skills = models.JSONField(default=list)
    primary_project_format = models.JSONField(default=list)
    manual_preferences = models.JSONField(default=list)
    has_submitted = models.BooleanField(default=False)
    
    # Existing allocation field (where the algorithm puts its final answers)
    allocated_supervisor = models.ForeignKey(
        'SupervisorProfile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='allocated_students'
    )

    has_pre_agreement = models.BooleanField(default=False)
    pre_agreed_supervisor = models.ForeignKey(
        'SupervisorProfile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='pre_agreements',
        help_text="The specific academic the student has a prior arrangement with."
    )

    def __str__(self):
        return self.name
    
class SystemConfiguration (models.Model) : 
    max_manual_preferences = models.IntegerField(
        default=3,
        help_text="Maximum number of manual preferences a student can submit"
    )
    def save(self, *args, **kwargs): 
        self.pk = 1 # Ensure only one instance exists
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        pass # prevent the module leader from accidentally deleting the settings.
    class Meta:
        # This make it look tidy in the admin panel ( removes the pluaral 's')
        verbose_name = "System Configuration"
        verbose_name_plural = "System Configuration"
