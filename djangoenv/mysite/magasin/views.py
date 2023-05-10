from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.shortcuts import redirect, render
from .forms import ProduitForm, FournisseurForm,UserRegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    list=produit.objects.all() 
    return render(request,'magasin/vitrine.html',{'list':list})

def AddProd(request):
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else:
        form = ProduitForm()
    produits = produit.objects.all()
    return render(request, 'magasin/majProduits.html', {'produits': produits, 'form': form})

def edit_product(request, product_id):
    p = produit.objects.get(id=product_id)
    form = ProduitForm(instance=p)
    
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    return render(request, 'magasin/edit_produit.html', {'form': form, 'produit': p})

def view_product(request, product_id):
    product = get_object_or_404(produit, id=product_id)
    return render(request, 'magasin/produit_detail.html', {'product': product})

def nouveauFournisseur(request):
    if request.method == "POST" : 
        form = FournisseurForm(request.POST,request.FILES) 
        if form.is_valid(): 
            form.save() 
            return HttpResponseRedirect('/magasin/affichefou') 
    else: 
        form = FournisseurForm() 
    fournisseurs=fournisseur.objects.all()
    return render(request,'magasin/testForm.html',{'fournisseurs':fournisseurs,'form':form})

@login_required
def affichefou(request):
    fou=fournisseur.objects.all()
    return render(request,'magasin/vitrine2.html',{'fou':fou})

def delete_product(request, product_id):
    # Récupérer le produit correspondant à l'identifiant unique donné
    product = get_object_or_404(produit, id=product_id)

    if request.method == 'POST':
        # Supprimer le produit de la base de données
        product.delete()
        return redirect('index')
    return render(request, 'magasin/delete_product.html', {'product': product})

def register(request):
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return redirect('home')
    else :
        form = UserCreationForm()
    return render(request,'registration/register.html',{'form' : form})


def view_fournisseur(request, fou_id):
    fou = get_object_or_404(fournisseur, id=fou_id)
    return render(request, 'magasin/fournisseur_detail.html', {'fournisseur': fou})

def edit_fournisseur(request, fou_id):
    f = fournisseur.objects.get(id=fou_id)
    form = FournisseurForm(instance=f)
    
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=f)
        if form.is_valid():
            form.save()
            return redirect('affichefou')
    
    return render(request, 'magasin/edit_fournisseur.html', {'form': form, 'fournisseur': f})

def delete_fou(request, fou_id):
    # Récupérer le produit correspondant à l'identifiant unique donné
    f = get_object_or_404(fournisseur, id=fou_id)

    if request.method == 'POST':
        # Supprimer le produit de la base de données
        f.delete()
        return redirect('affichefou')
    return render(request, 'magasin/delete_fournisseur.html', {'fournisseur': f})
#panier

# def add_to_cart(request, product_id):
#     p = get_object_or_404(produit, id=product_id)
#     panier, created = Panier.objects.get_or_create(user=request.user, produit=p)
#     if not created:
#         panier.quantite += 1
#         panier.save()
#     return redirect('cart')

# def cart(request):
#     paniers = Panier.objects.filter(user=request.user)
#     total = 0
#     for panier in paniers:
#         panier.prix_total = panier.produit.prix * panier.quantite
#         panier.save()
#         total += panier.prix_total
#     return render(request, 'magasin/Panier/cart.html', {'paniers': paniers, 'total': total})

# def checkout(request):
#     paniers = Panier.objects.filter(user=request.user)
#     commande = command(user=request.user)
#     commande.save()
#     for panier in paniers:
#         detail = LigneCommande(commande=commande, produit=panier.produit, quantite=panier.quantite, prix_unitaire=panier.produit.prix, prix_total=panier.prix_total)
#         detail.save()
#         panier.delete()
#     return redirect('commande_detail', commande.id)

# def commande_detail(request, commande_id):
#     commande = get_object_or_404(command, id=commande_id, user=request.user)
#     lignes_commande = LigneCommande.objects.filter(commande=commande)
#     return render(request, 'magasin/Panier/commande_detail.html', {'commande': commande, 'lignes_commande': lignes_commande})
