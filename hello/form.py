from django import forms

class FindTrend(forms.Form):
   search_term = forms.CharField(max_length=1000)