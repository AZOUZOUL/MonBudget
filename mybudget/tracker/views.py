from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Connecter l'utilisateur automatiquement après l'inscription
            login(request, user)
            return redirect('/') # Redirige vers la page d'accueil/tableau de bord
    else:
            form = UserCreationForm()
    return render(request, 
                      'tracker/signup.html',
                      {"form": form})
