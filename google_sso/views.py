from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from google.oauth2 import id_token 
from google.auth.transport import requests as google_requests 
from .forms import EssayForm
from .models import Essay, Prompt
import openai # type: ignore
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
    # print("Title:", title)
    # print("Body:", body)
    

    try:
        spelling_prompt = Prompt.objects.get(name='spelling_prompt').prompt_text
        content_prompt = Prompt.objects.get(name='content_prompt').prompt_text
        score_prompt = Prompt.objects.get(name='score_prompt').prompt_text
    except Prompt.DoesNotExist:
        print("Fallback prompts used.")
        # Default prompts in case they are not found in the database
        spelling_prompt = "Check the following essay for spelling errors and provide the incorrectly spelled words along with their index positions.\n\nEssay:\n{body}"
        content_prompt = "Is the content of the following essay related to its title? Answer in Yes or No. Title: {title}\n\nEssay:\n{body}"
        score_prompt = "Based on spelling mistakes and topic relevance, provide an integer score out of 10 for the essay. Title: {title}\n\nEssay:\n{body}"
    
    # print("Spelling Prompt:", spelling_prompt)
    # print("Content Prompt:", content_prompt)
    # print("Score Prompt:", score_prompt)
    
    # Check spelling errors
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=spelling_prompt.format(body=body),
        max_tokens=500
    )
    spelling_feedback = response.choices[0].text.strip()

    # Check if the content is related to the title
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=content_prompt.format(title=title, body=body),
        max_tokens=10
    )
    content_related = response.choices[0].text.strip()

    # Provide an essay score out of 10
    score_prompt = Prompt.objects.get(name='score_prompt').prompt_text
    score_response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=score_prompt.format(title=title, body=body),
        max_tokens=10
    )
    score_text = score_response.choices[0].text.strip()
    score_match = re.search(r'\d+', score_text)
    if score_match:
        score = int(score_match.group())
    else:
        # Handle the case where no digit is found (default to 0 or raise an error)
        score = 0  # Example: Default to 0

    return {
        'spelling_feedback': spelling_feedback,
        'content_related': content_related,
        'score': score
    }

@csrf_exempt    
def google_login(request):
    token = request.POST.get('credential', None)
    if token is None:
        return JsonResponse({'error': 'Token not provided'}, status=400)

    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), os.environ.get('GOOGLE_CLIENT_ID'))
        userid = idinfo['sub']
        email = idinfo.get('email')
        first_name = idinfo.get('given_name')
        last_name = idinfo.get('family_name')

        user, created = User.objects.get_or_create(username=userid, defaults={'first_name': first_name, 'last_name': last_name, 'email': email})

        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    except ValueError:
        return JsonResponse({'error': 'Invalid token'}, status=400)