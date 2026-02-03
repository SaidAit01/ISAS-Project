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
    manual_preferences= models.JSONField(default= list)

def __str__(self):
        return f"{self.name} (Cap: {self.capacity})"

