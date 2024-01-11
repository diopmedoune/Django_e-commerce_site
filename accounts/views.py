# accounts/views.py

from django.shortcuts import render, redirect
from  django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Les mots de passe ne correspondes pas. Réessayez svp !')

    return render(request, 'accounts/signup.html')


from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request," Nom d'utilisateur ou mot de passe incorrect. Réesayez svp !")
    
    return render(request, 'accounts/login.html')



def logout_user(request):
    logout(request)
    return redirect('index')