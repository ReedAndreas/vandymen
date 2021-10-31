from django import forms
from statsApp.models import Team
from django.utils.safestring import mark_safe

class SearchForm(forms.Form):
    search_value = forms.CharField(label='', max_length=100)

class MatchupPredictor(forms.Form):
    team1 = forms.ModelChoiceField(queryset=Team.objects.all())
    team2 = forms.ModelChoiceField(queryset=Team.objects.all())
