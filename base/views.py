from django.shortcuts import render, redirect
import requests
from requests import get
from .models import Message, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm, UserForm


# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User Doesn\'t Exist')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
    context = {'form':form}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def index(request):
    user = request.user
    user_messages = user.message_set.all().order_by('-created')
    if request.method == 'POST':
        body = request.POST.get('msg')
        url = "http://api.brainshop.ai/get?bid=157984&key=3S0hhLXZ5GS2KYs4&uid=[uid]&msg=[{}]".format(body)
        response = requests.get(url).json()['cnt']
        message = Message.objects.create(user=user, body=body, res=response)
        # return redirect('chat')
    context = {'user_messages': user_messages}
    return render(request, 'base/home.html', context)

def home(request):
    return render(request, 'base/index.html')

def about(request):
    return render(request, 'base/about.html')

def userProfile(request):
    user = User.objects.get(id=request.user.id)
    context = {'user':user}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
    context = {'form':form}
    return render(request, 'base/update-user.html', context)
