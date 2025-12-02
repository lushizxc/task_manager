from django.db import models
from django.contrib.auth.models import User
from datetime import date

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
    media = models.FileField(upload_to='tasks_media/',blank=True,null=True)

    @property
    def is_overdue(self):
        if not self.due_date:
            return False
        return self.due_date < date.today() and self.status != 'done'

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='comments_media/',blank=True,null=True)

    def __str__(self):
        return f'{self.author}: {self.text}'