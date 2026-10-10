from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from tracker.models import Categorie, Transaction
from tracker.forms import TransactionForm, CategorieForm



def inscription(request):
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
                      'tracker/inscription.html',
                      {"form": form})

@login_required
def demander_deconnexion(request):
    return render(request,
           'tracker/demander_deconnexion.html',)

@login_required
def deconnexion(request):
    return render(request,
                  'tracker/deconnexion.html',)
    

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
# --- Nouvelle vue du J4 ---
@login_required
def accueil(request):
    
    #======                             =======
    #          Calcul du Mois Courant
    #======                             ========
    # Détection automatique de la date du jour réelle
    maintenant = timezone.now()
    annee_actuelle = maintenant.year
    mois_actuel = maintenant.month
    # Filtrage cumulé (Cloisonnement Utilisateur J4 + Mois en cours)
    mes_transactions_actuelles = Transaction.objects.filter(
        utilisateur=request.user,
        date__year=annee_actuelle,  # Extrait uniquement l'année en cours
        date__month=mois_actuel,  # Extrait uniquement le mois en cours
    )
    # Calculs automatiques basés uniquement sur les données du mois filtré
    entrees_actuelles = sum(transaction.montant for transaction in mes_transactions_actuelles if transaction.categorie.type == 'REV')
    depenses_actuelles = sum(transaction.montant for transaction in mes_transactions_actuelles if transaction.categorie.type == "DEP")
    solde_du_mois_actuel = entrees_actuelles - depenses_actuelles
    #======             ======
    #           Fin
    #======             ======

    return render(
        request,
        "tracker/accueil.html",
        {
            "transactions_actuelles": mes_transactions_actuelles,
            "entrees_actuelles": entrees_actuelles,
            "depenses_actuelles": depenses_actuelles,
            "solde_du_mois_actuel": solde_du_mois_actuel,
            "date_actuelle": maintenant,
        },
    )
    
@login_required
def transactions(request):
    mes_categories = Categorie.objects.filter(utilisateur=request.user)
    return render(request,
                  "tracker/transactions.html",
                  {"categories": mes_categories})
    
@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.utilisateur = request.user
            transaction.save()
            return redirect('accueil')
    else:
        form = TransactionForm(user=request.user)
        
    return render(request,
                  'tracker/transaction_create.html',
                  {'form': form})

@login_required
def transaction_update(request, pk):
    # Sécurité : On cherche la transaction par son ID (pk) ET on valide qu'elle appartient au connecté
    transaction = get_object_or_404(Transaction, pk=pk, utilisateur=request.user)
    
    if request.method == 'POST':
        # On passe l'instance existante au formulaire pour que Django pré-remplisse les cases
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            # Notification flash de succès
            messages.success(request, "La transaction a été modifiée avec succès.")
            return redirect('transactions')
        else:
            # Si le formulaire a échoué
            messages.error(request, "Échec de la modification. Veuillez vérifier vos données.")
    else:
        form = TransactionForm(instance=transaction, user=request.user)
        
    return render(request, 'tracker/transaction_update.html', {'form': form, 'transaction': transaction})

@login_required
def transaction_delete(request, pk):
    # Sécurité : Idem, impossible de supprimer la ligne d'un autre utilisateur
    transaction = get_object_or_404(Transaction, pk=pk, utilisateur=request.user)

    if request.method == "POST":
        # Si l'utilisateur valide le formulaire de confirmation (POST), on supprime
        transaction.delete()
        messages.success(request, "La transaction a bien été supprimée.")
        return redirect("transactions")

    # Si c'est un GET, on affiche simplement la page de confirmation épurée
    return render(
        request, "tracker/transaction_delete.html", {"transaction": transaction}
    )
    
@login_required
def categories(request):
    mes_categories = Categorie.objects.filter(utilisateur=request.user)
    return render(
        request,
        "tracker/categories.html",
        {
            "categories": mes_categories,
        },
    )
    
@login_required
def categorie_create(request):
    if request.method == "POST":
        form = CategorieForm(request.POST)
        if form.is_valid():
            # commit=False bloque l'enregistrement immédiat en BDD
            categorie = form.save(commit=False)
            # Sécurité : On injecte de force l'identité de l'utilisateur connecté
            categorie.utilisateur = request.user
            # Sauvegarde définitive en base de données
            categorie.save()

            # Notification de succès (J6)
            messages.success(
                request, f"La catégorie '{categorie.nom}' a été créée avec succès."
            )

            # Redirection automatique vers la liste des catégories après l'ajout
            return redirect("categories")
    else:
        # Si c'est un GET, on prépare un formulaire de création vierge
        form = CategorieForm()

    return render(request,
                  "tracker/categorie_create.html",
                  {"form": form})

@login_required
def categorie_update(request, pk):
    # Impossible de modifier la catégorie d'un autre utilisateur
    categorie = get_object_or_404(Categorie, pk=pk, utilisateur=request.user)

    if request.method == "POST":
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, "La catégorie a bien été mise à jour.")
            return redirect("categories")
    else:
        form = CategorieForm(instance=categorie)

    return render(
        request,
        "tracker/categorie_update.html",
        {"form": form, "categorie": categorie},
    )

@login_required
def categorie_delete(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk, utilisateur=request.user)

    # L'élément clé du J7 : On compte le nombre de transactions liées
    nombre_transactions = categorie.transaction_set.count

    if request.method == "POST":
        if nombre_transactions > 0:
            # Refus catégorique si des transactions dépendent de cette catégorie
            messages.error(
                request,
                f"Impossible de supprimer. Cette catégorie contient {nombre_transactions} transaction(s).",
            )
            return redirect("categories")

        # Si aucun lien, on valide la suppression
        categorie.delete()
        messages.success(request, "La catégorie a bien été supprimée.")
        return redirect("categories")

    return render(
        request,
        "tracker/categorie_delete.html",
        {"categorie": categorie, "nombre_transactions": nombre_transactions},
    )