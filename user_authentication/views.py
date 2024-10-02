from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import CreateUserForm

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}')

                return redirect('login')
        context = {'form': form}
        return render(request, 'registration/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'registration/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url= "login")
def home(request):
    user_lat = request.GET.get('user_lat', '0')  # Default to 0 if not provided
    user_lng = request.GET.get('user_lng', '0')  # Default to 0 if not provided
    context = {
        'user': request.user,
        'user_lat': user_lat,
        'user_lng': user_lng,
    }
    return render(request, 'home/home.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        # Handle password change
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')

        # Handle username and email change
        username = request.POST.get('username')
        email = request.POST.get('email')
        user = request.user
        if username and username != user.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken.')
            else:
                user.username = username
                user.save()
                messages.success(request, 'Your username was successfully updated!')
        if email and email != user.email:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already in use.')
            else:
                user.email = email
                user.save()
                messages.success(request, 'Your email was successfully updated!')

        return redirect('profile')

    else:
        password_form = PasswordChangeForm(request.user)

    return render(request, 'profile/profile.html', {
        'password_form': password_form,
    })
def restaurant_detail(request, place_id):
    # Fetch restaurant details using the place_id
    # Render the details template
    return render(request, 'restaurant_search/restaurant_detail.html', {'place_id': place_id})