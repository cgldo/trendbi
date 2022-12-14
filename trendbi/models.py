from django.db import models
from django import forms

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
    
class FindTrend(forms.Form):
   search_term = forms.CharField(max_length=1000)
   start_field = models.DateField()
   end_field = models.DateField()
   google = forms.BooleanField()
   youtube = forms.BooleanField()
   twitter = forms.BooleanField()
   numbers = models.IntegerField()
