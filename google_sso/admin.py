# admin.py
from django.contrib import admin
from .models import Prompt, Essay
from .forms import EssayForm

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('name', 'prompt_text')

