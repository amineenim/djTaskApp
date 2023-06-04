from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model) :
    # define a many to one relationship, numerous tasks can belong to same user
    # in db this value can be null, and in form submission it can be blank
    user = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE, null= True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True )
    complete = models.BooleanField(default=False)
    # when an item is created, the time is automatically added 
    created_at = models.DateTimeField(auto_now_add= True)

    # the representation for the model 
    def __str__(self) : 
        return self.title 
    
    class Meta : 
        # order the items by the complete status, completed are at the bottom of the list
        ordering = ['complete']
        
    

