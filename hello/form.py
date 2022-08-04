from django import forms

class ContactUsForm(forms.Form):
   search_term = forms.CharField(max_length=1000)