from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .forms import CreateUserForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from favorites.models import Favorite
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

@login_required
@require_POST
def toggle_favorite(request):
    place_id = request.POST.get('place_id')
    name = request.POST.get('name')
    image_url = request.POST.get('image_url')
    rating = request.POST.get('rating')
    address = request.POST.get('address')
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        place_id=place_id,
        defaults={'name': name,
                  'image_url': image_url,
                  'rating': rating,
                  'address': address
                  }
    )
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})
@login_required
def favorites(request):
    user_favorites = Favorite.objects.filter(user=request.user).order_by('-added_on')
    return render(request, 'user_authentication/favorites.html', {'favorites': user_favorites})