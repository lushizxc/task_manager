from django import forms
from .models import *

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','status','priority','due_date','media']

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text','media']
        widgets = {'media': forms.FileInput()}