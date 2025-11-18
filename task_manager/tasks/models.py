from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo','To Do'),
        ('in progress', 'In Progress'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('high','High'),
        ('mid',"Mid"),
        ('low','Low'),

    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=11,choices=STATUS_CHOICES,default="todo")
    priority = models.CharField(max_length=11,choices=PRIORITY_CHOICES,default='mid')
    due_date = models.DateField(null=True,blank=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')

    def __str__(self):
        return self.title

