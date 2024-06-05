from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from google.oauth2 import id_token 
from google.auth.transport import requests as google_requests 
from .forms import EssayForm
from .models import Essay, Prompt
import openai
import re
import os
from django.views.decorators.csrf import csrf_exempt


def home(request):
    # Check if user is authenticated
    if request.user.is_authenticated:
        context = {'user': request.user}  # Include user object in context
    else:
        context = {}  # Empty context for anonymous users
    return render(request, 'home.html', context)

@login_required
def submit_essay(request):
    
    if request.method == 'POST':
        form = EssayForm(request.POST)
        if form.is_valid():
            api_key = form.cleaned_data['api_key']
            essay = form.save(commit=False)
            essay.user = request.user
            feedback = evaluate_essay(api_key, essay.title, essay.body)
            essay.spelling_feedback = feedback['spelling_feedback']
            essay.content_related = feedback['content_related']
            essay.score = feedback['score']
            essay.save()
            return render(request, 'essay_feedback.html', {'essay': essay, 'feedback': feedback})
    else:
        form = EssayForm()
    return render(request, 'submit_essay.html', {'form': form})

@login_required
def essay_list(request):
    essays = Essay.objects.filter(user=request.user)
    return render(request, 'essay_list.html', {'essays': essays})

def evaluate_essay(api_key, title, body):
    openai.api_key = api_key

    try:
        spelling_prompt = Prompt.objects.get(name='spelling_prompt').prompt_text
        content_prompt = Prompt.objects.get(name='content_prompt').prompt_text
        score_prompt = Prompt.objects.get(name='score_prompt').prompt_text
    except Prompt.DoesNotExist:
        print("Fallback prompts used.")
        spelling_prompt = "Check the following essay for spelling errors and provide the incorrectly spelled words along with their index positions.\n\nEssay:\n{body}"
        content_prompt = "Is the content of the following essay related to its title? Answer in Yes or No. Title: {title}\n\nEssay:\n{body}"
        score_prompt = "Based on spelling mistakes and topic relevance, provide an integer score out of 10 for the essay. Title: {title}\n\nEssay:\n{body}"
    
    # Check spelling errors
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a spelling checker."},
            {"role": "user", "content": spelling_prompt.format(body=body)}
        ],
        max_tokens=500
    )
    spelling_feedback = response.choices[0]['message']['content'].strip()

    # Check if the content is related to the title
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a content relevance checker."},
            {"role": "user", "content": content_prompt.format(title=title, body=body)}
        ],
        max_tokens=10
    )
    content_related = response.choices[0]['message']['content'].strip()

    # Provide an essay score out of 10
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an essay scorer."},
            {"role": "user", "content": score_prompt.format(title=title, body=body)}
        ],
        max_tokens=10
    )
    score_text = response.choices[0]['message']['content'].strip()
    score_match = re.search(r'\d+', score_text)
    score = int(score_match.group()) if score_match else 0

    return {
        'spelling_feedback': spelling_feedback,
        'content_related': content_related,
        'score': score
    }