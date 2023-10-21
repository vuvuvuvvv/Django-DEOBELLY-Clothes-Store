from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from .forms import SignUpForm, CompleteInformationForm
from .models import User
from django.http import JsonResponse
import json
# Create your views here.
def signup(req):
    if req.user.is_authenticated:
        return redirect('home')
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            user = form.save()
            user = User.objects.get(pk=req.user.id)
            user.is_verified = 1
            user.save()
            auth_login(req, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(req,'signup.html',{'form':form})

def validate_infor_user(req):
    if req.method == 'POST':
        form = CompleteInformationForm(req.POST, instance=req.user)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            instance_user = User.objects.get(pk=req.user.id)
            instance_user.is_verified = 1
            instance_user.username = username
            instance_user.tel = form.cleaned_data['tel']
            instance_user.set_password(password)
            instance_user.save()
            user = authenticate(req, username, password)
            if user:
                auth_login(req, user,backend='django.contrib.auth.backends.ModelBackend')
            else:
                return redirect('validate_infor_user')
        return redirect('home')
    else:    
        if req.user.is_authenticated:
            if req.user.is_verified or req.user.is_superuser:
                return redirect('home')
            else:
                form = CompleteInformationForm()
                return render(req,'complete_information.html',{'form':form})
        else:
            return redirect('login')

def check_user_validated(req):
    if req.method == "POST":
        data = json.loads(req.body)
        try:
            user = get_object_or_404(User, email = data['email'])
            result = {
                'is_verified' : True if user.is_verified == 1 else False
            }
        except Exception:
            result = {
                'undefind' : True
            }
        return JsonResponse(result)