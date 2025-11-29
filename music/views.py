from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html')
    
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

def logout(request):
    auth.logout(request)
    return redirect('login')
