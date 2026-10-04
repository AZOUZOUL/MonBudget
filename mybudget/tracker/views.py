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
    
"""
    <<< Ceci est le code que je voulais utiliser pour
    créer une conexion personnaliser avant de savoir que ce n'est pas la peine
    >>>
    
    def log_in(request):
    if request.method == "POST":
        # 1. On remplit le formulaire avec les données saisies par l'utilisateur
        form = AuthenticationForm(request, data=request.POST)
        
        # 2. On vérifie si les identifiants respectent les règles de base
        if form.is_valid():
            # 3. On extrait le pseudo et le mot de passe nettoyés
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 4. Le module authenticate vérifie en BDD si le couple pseudo/mot de passe est correct
            user = authenticate(username, password)
            
            if user is not None:
                # 5. Si l'utilisateur existe, la fonction login crée sa session de connexion
                login(request, user)
                return redirect('/') # Redirection vers la page d'accueil
    else:
    # Si c'est un GET, on prépare un formulaire de connexion vide
        form = AuthenticationForm()

    return render(request, 
                      'tracker/login.html',
                      {'form': form})
"""