"""
URL configuration for mybudget project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from tracker import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # La route racine '/' appelle maintenant votre vue sécurisée
    path("", views.accueil, name="accueil"),
    path("transactions/add/", views.transaction_create, name="transaction-create"),
    path("accounts/inscription/", views.inscription, name="inscription"),
    
    # CORRECTION 1 : On utilise l'adresse attendue par Django /login/ et le name="login"
    # CORRECTION 2 : Assurez-vous que votre fichier s'appelle bien "connexion.html" si vous écrivez ceci :
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="tracker/connexion.html"),
        name="login",
    ),
    # La route de déconnexion automatique
    path(
        "accounts/demander_deconnexion/",
        views.demander_deconnexion,
        name="demander-deconnexion",
    ),
    path("accounts/deconnexion/", views.deconnexion, name="deconnexion"),
    path("accounts/", include("django.contrib.auth.urls")),
]
