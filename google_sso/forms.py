# forms.py
from django import forms
from .models import Essay

class EssayForm(forms.ModelForm):
    api_key = forms.CharField(max_length=100, required=True, help_text='Enter your OpenAI API key.')

    class Meta:
        model = Essay
        fields = ['title', 'body', 'api_key']

    def clean_body(self):
        body = self.cleaned_data['body']
        word_count = len(body.split())
        if word_count > 500:
            raise forms.ValidationError('The essay body cannot exceed 500 words. Current word count: {}'.format(word_count))
        return body