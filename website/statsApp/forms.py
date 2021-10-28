from django import forms

class SearchForm(forms.Form):
    search_value = forms.CharField(label='', max_length=100)
