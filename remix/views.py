from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import requests
import urllib.parse
import os
# Create your views here.

def spotify_login(request):
    auth_url = 'https://accounts.spotify.com/authorize'
    client_id = settings.SPOTIFY_CLIENT_ID
    redirect_uri = 'http://localhost:8000/callback/'
    scope = 'user-read-email playlist-read-private playlist-modify-public'

    auth_query_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope,
    }

    auth_query = f"{auth_url}?{urllib.parse.urlencode(auth_query_params)}"
    return redirect(auth_query)

def spotify_callback(request):
    code = request.GET.get('code')

    if code is None:
        return JsonResponse({'/error'})
    
    token_url = 'https://accounts.spotify.com/api/token'
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    redirect_uri = 'http://localhost:8000/callback/'

    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(token_url, data=token_data)
    token_response_data = response.json()

    if 'access_token' not in token_response_data:
        return redirect('/error')
    
    access_token = token_response_data['access_token']
    request.session['spotify_access_token'] = access_token
    return HttpResponse("Authentication successful!")

def error_view(request):
    return HttpResponse("An error occured during authentication. Please try again", status = 400)