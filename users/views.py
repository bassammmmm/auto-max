from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.views import View
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        login_form = MyAuthenticationForm(request = request, data = request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Logged in as {username}')
                return redirect('home')
        else:
            messages.error(request, f'Invalid username or password')
            return redirect('login')
            
    login_form = MyAuthenticationForm()
    context = {
        'login_form' : login_form
    }
    return render(request, 'views/login.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('main')

class RegisterView(View):
    def get(self, request):
        register_form = ExtendedUserCreationForm()
        context = {
            'register_form' : register_form
        }
        return render(request, 'views/register.html', context)
    
    def post(self,request):
        register_form = ExtendedUserCreationForm(request.POST)
        if register_form.is_valid():
            try: #We had to make this try except to ignore the DataError that comes from the Heroku Postgresql Database as a bug and it creates the user anyway.
                user = register_form.save()
            except Exception as e:
                user = register_form.save()
            user.refresh_from_db()
            login(request, user)
            messages.success(request, f'Your account has been created and logged in as {user.username} successfully!')
            return redirect('home')
        else:
            context = {
                'register_form' : register_form
            }
            return render(request, 'views/register.html', context)