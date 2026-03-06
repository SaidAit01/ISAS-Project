from django.db import models


# models containd the essentisl fields and behaviour of the data
class SupervisorProfile(models.Model) : 
    name = models.CharField(max_length=100)
    research_interests = models.TextField() 
    capacity = models.IntegerField(default=5)

    def __str__(self):
        return self.name

class StudentProposal (models.Model) : 
    name = models.CharField(max_length=100)
    topic_description = models.TextField()
    manual_preferences= models.JSONField(default=list)

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
