# forms.py
from django import forms
from .models import Essay

class EssayForm(forms.ModelForm):
    api_key = forms.CharField(max_length=100, required=True, help_text='Enter your OpenAI API key.')

    class Meta:
        model = Essay
        fields = ['title', 'body', 'api_key']