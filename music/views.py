from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from artists_data import top_artists
from tracks_data import top_tracks 
import requests
import os

load_dotenv()

        


@login_required(login_url='login')
def index(request):
    first_six_tracks = top_tracks[:6]
    second_six_tracks = top_tracks[6:12]
    third_six_tracks = top_tracks[12:18]

    context = {
        'artists_info' : top_artists,
        'first_six_tracks': first_six_tracks,
        'second_six_tracks': second_six_tracks,
        'third_six_tracks': third_six_tracks,
    }

    return render(request, 'index.html', context)
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
        elif User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.info(request, 'User already exists')
            return redirect('login')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            auth.login(request, user)
            return redirect('/')
    return render(request, 'signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def get_audio_details(query):
    url = "https://spotify-scraper.p.rapidapi.com/v1/track/download/soundcloud"

    querystring = {"track": query,"quality":"sq"}

    headers = {
        "x-rapidapi-key": "c76c79dc85msh58c487ff509dc7ap1cdd5bjsn5f2523f93b17",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    audio_details = []
    if response.status_code == 200:
        data = response.json()
        track = data.get("soundcloudTrack")
        if track and "audio" in track and track["audio"]:
            first_audio = track["audio"][0]
            audio_details.append(first_audio.get("url"))
            audio_details.append(first_audio.get("durationText"))


    return audio_details
    

@login_required(login_url='login')
def music(request, pk):
    url = f'https://api.spotify.com/v1/tracks/{pk}'
    headers = {
        'Authorization': f'Bearer {os.getenv('SPOTIFY_TOKEN')}',
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'album' in data:
            track_name = data.get('name')
            artists = data.get('artists', [])
            first_artist_name = artists[0].get('name') if artists else 'Unknown'
            audio_details = get_audio_details(track_name + first_artist_name)
            audio_url = audio_details[0]
            duration_text = audio_details[1]
            context = {
                'track_name': track_name,
                'artist_name': first_artist_name,
                'audio_url': audio_url,
                'duration_text': duration_text,
            }
    return render(request, 'music.html', context)