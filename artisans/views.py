
from django.shortcuts import render, get_object_or_404, redirect
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Artisan, Produit, Vente, Commande, Categorie
from .forms import ArtisanForm, ProduitForm, VenteForm, CommandeForm, CategorieForm, RechercheForm

@login_required
def commande_create(request):
    """Créer une nouvelle commande"""
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save()
            messages.success(request, f'Commande créée avec succès!')
            return redirect('artisans:commande_list')
    else:
        form = CommandeForm()
    context = {
        'form': form,
        'title': 'Créer une commande',
    }
    return render(request, 'artisans/commande_form.html', context)
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Artisan, Produit, Vente, Commande, Categorie
from .forms import ArtisanForm, ProduitForm, VenteForm, CommandeForm, CategorieForm, RechercheForm

def home(request):
    """Page d'accueil avec statistiques et aperçu"""
    # Statistiques générales
    total_artisans = Artisan.objects.filter(actif=True).count()
    total_produits = Produit.objects.filter(disponible=True).count()
    total_ventes = Vente.objects.filter(statut='confirmee').aggregate(total=Sum('montant'))['total'] or 0
    
    # Ventes du mois
    debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    ventes_mois = Vente.objects.filter(
        date_vente__gte=debut_mois,
        statut='confirmee'
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    # Produits récents
    produits_recents = Produit.objects.filter(disponible=True).order_by('-date_creation')[:6]
    
    # Artisans populaires
    artisans_populaires = Artisan.objects.filter(actif=True).annotate(
        total_ventes_annotated=Sum('ventes__montant')
    ).order_by('-total_ventes_annotated')[:5]
    
    # Catégories populaires
    categories_populaires = Categorie.objects.annotate(
        nombre_produits=Count('produits')
    ).order_by('-nombre_produits')[:6]
    
    context = {
        'total_artisans': total_artisans,
        'total_produits': total_produits,
        'total_ventes': total_ventes,
        'ventes_mois': ventes_mois,
        'produits_recents': produits_recents,
        'artisans_populaires': artisans_populaires,
        'categories_populaires': categories_populaires,
    }
    return render(request, 'artisans/home.html', context)

def artisan_list(request):
    """Liste des artisans avec recherche et filtres"""
    artisans = Artisan.objects.filter(actif=True)
    
    # Recherche
    q = request.GET.get('q')
    if q:
        artisans = artisans.filter(
            Q(nom__icontains=q) |
            Q(specialite__icontains=q) |
            Q(description__icontains=q)
        )
    
    # Filtre par spécialité
    specialite = request.GET.get('specialite')
    if specialite:
        artisans = artisans.filter(specialite__icontains=specialite)
    
    # Pagination
    paginator = Paginator(artisans, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistiques
    stats = {
        'total': artisans.count(),
        'specialites': Artisan.objects.values_list('specialite', flat=True).distinct()
    }
    
    context = {
        'page_obj': page_obj,
        'stats': stats,
        'search_query': q,
        'selected_specialite': specialite,
    }
    return render(request, 'artisans/artisan_list.html', context)

def artisan_detail(request, artisan_id):
    """Détail d'un artisan avec ses produits et statistiques"""
    artisan = get_object_or_404(Artisan, id=artisan_id)
    produits = artisan.produits.filter(disponible=True)
    ventes = artisan.ventes.all()[:10]  # 10 dernières ventes
    
    # Statistiques de l'artisan
    stats = {
        'total_ventes': artisan.total_ventes,
        'nombre_produits': artisan.nombre_produits,
        'nombre_ventes': artisan.ventes.count(),
        'moyenne_prix': artisan.produits.aggregate(avg=Sum('prix')/Count('prix'))['avg'] or 0
    }
    
    context = {
        'artisan': artisan,
        'produits': produits,
        'ventes': ventes,
        'stats': stats,
    }
    return render(request, 'artisans/artisan_detail.html', context)

def produit_list(request):
    """Liste des produits avec recherche et filtres"""
    produits = Produit.objects.filter(disponible=True)
    form = RechercheForm(request.GET)
    
    if form.is_valid():
        q = form.cleaned_data.get('q')
        categorie = form.cleaned_data.get('categorie')
        prix_min = form.cleaned_data.get('prix_min')
        prix_max = form.cleaned_data.get('prix_max')
        
        if q:
            produits = produits.filter(
                Q(nom__icontains=q) |
                Q(description__icontains=q) |
                Q(artisan__nom__icontains=q)
            )
        
        if categorie:
            produits = produits.filter(categorie=categorie)
        
        if prix_min:
            produits = produits.filter(prix__gte=prix_min)
        
        if prix_max:
            produits = produits.filter(prix__lte=prix_max)
    
    # Pagination
    paginator = Paginator(produits, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'categories': Categorie.objects.all(),
    }
    return render(request, 'artisans/produit_list.html', context)

def produit_detail(request, produit_id):
    """Détail d'un produit"""
    produit = get_object_or_404(Produit, id=produit_id)
    produits_similaires = Produit.objects.filter(
        categorie=produit.categorie,
        disponible=True
    ).exclude(id=produit.id)[:4]
    
    context = {
        'produit': produit,
        'produits_similaires': produits_similaires,
    }
    return render(request, 'artisans/produit_detail.html', context)

def vente_list(request):
    """Liste des ventes avec filtres"""
    ventes = Vente.objects.all()
    
    # Filtres
    artisan_id = request.GET.get('artisan')
    statut = request.GET.get('statut')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    if artisan_id:
        ventes = ventes.filter(artisan_id=artisan_id)
    
    if statut:
        ventes = ventes.filter(statut=statut)
    
    if date_debut:
        ventes = ventes.filter(date_vente__date__gte=date_debut)
    
    if date_fin:
        ventes = ventes.filter(date_vente__date__lte=date_fin)
    
    # Pagination
    paginator = Paginator(ventes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistiques
    total_ventes = ventes.aggregate(total=Sum('montant'))['total'] or 0
    nb_ventes = ventes.count()
    moyenne_vente = (total_ventes / nb_ventes) if nb_ventes else 0
    # Ventes de la semaine (7 derniers jours)
    debut_semaine = timezone.now() - timedelta(days=7)
    ventes_semaine = ventes.filter(date_vente__gte=debut_semaine).aggregate(total=Sum('montant'))['total'] or 0
    context = {
        'page_obj': page_obj,
        'total_ventes': total_ventes,
        'moyenne_vente': moyenne_vente,
        'ventes_semaine': ventes_semaine,
        'artisans': Artisan.objects.filter(actif=True),
        'statuts': Vente._meta.get_field('statut').choices,
    }
    return render(request, 'artisans/vente_list.html', context)

def vente_detail(request, vente_id):
    """Détail d'une vente"""
    vente = get_object_or_404(Vente, id=vente_id)
    
    context = {
        'vente': vente,
    }
    return render(request, 'artisans/vente_detail.html', context)

def commande_list(request):
    """Liste des commandes avec filtres"""
    commandes = Commande.objects.all()
    # Filtres
    q = request.GET.get('q', '').strip()
    artisan_id = request.GET.get('artisan')
    statut = request.GET.get('statut')

    if q:
        commandes = commandes.filter(
            Q(client_nom__icontains=q) |
              Q(artisan__nom__icontains=q) |
              Q(description__icontains=q)
        )
    if artisan_id:
        commandes = commandes.filter(artisan_id=artisan_id)
    if statut:
        commandes = commandes.filter(statut=statut)
    
    # Pagination
    paginator = Paginator(commandes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'artisans': Artisan.objects.filter(actif=True),
        'statuts': Commande._meta.get_field('statut').choices,
    }
    return render(request, 'artisans/commande_list.html', context)

# Vues pour l'ajout/modification (avec login_required)
@login_required
def artisan_create(request):
    """Créer un nouvel artisan"""
    if request.method == 'POST':
        form = ArtisanForm(request.POST, request.FILES)
        if form.is_valid():
            artisan = form.save()
            messages.success(request, f'Artisan "{artisan.nom}" créé avec succès!')
            return redirect('artisans:artisan_detail', artisan_id=artisan.id)
    else:
        form = ArtisanForm()
    
    context = {
        'form': form,
        'title': 'Ajouter un artisan',
    }
    return render(request, 'artisans/artisan_form.html', context)

@login_required
def artisan_update(request, artisan_id):
    """Modifier un artisan"""
    artisan = get_object_or_404(Artisan, id=artisan_id)
    
    if request.method == 'POST':
        form = ArtisanForm(request.POST, request.FILES, instance=artisan)
        if form.is_valid():
            artisan = form.save()
            messages.success(request, f'Artisan "{artisan.nom}" modifié avec succès!')
            return redirect('artisans:artisan_detail', artisan_id=artisan.id)
    else:
        form = ArtisanForm(instance=artisan)
    
    context = {
        'form': form,
        'artisan': artisan,
        'title': f'Modifier {artisan.nom}',
    }
    return render(request, 'artisans/artisan_form.html', context)

@login_required
def produit_create(request):
    """Créer un nouveau produit"""
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save()
            messages.success(request, f'Produit "{produit.nom}" créé avec succès!')
            return redirect('artisans:produit_detail', produit_id=produit.id)
    else:
        form = ProduitForm()
    
    context = {
        'form': form,
        'title': 'Ajouter un produit',
    }
    return render(request, 'artisans/produit_form.html', context)

@login_required
def produit_update(request, produit_id):
    """Modifier un produit"""
    produit = get_object_or_404(Produit, id=produit_id)
    
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            produit = form.save()
            messages.success(request, f'Produit "{produit.nom}" modifié avec succès!')
            return redirect('artisans:produit_detail', produit_id=produit.id)
    else:
        form = ProduitForm(instance=produit)
    
    context = {
        'form': form,
        'produit': produit,
        'title': f'Modifier {produit.nom}',
    }
    return render(request, 'artisans/produit_form.html', context)

@login_required
def vente_create(request):
    """Créer une nouvelle vente"""
    montant_initial = 0
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save(commit=False)
            produit = vente.produit
            vente.prix_unitaire = produit.prix
            vente.montant = vente.quantite * vente.prix_unitaire
            vente.save()
            messages.success(request, f'Vente enregistrée avec succès!')
            return redirect('artisans:vente_detail', vente_id=vente.id)
        else:
            # Si le formulaire n'est pas valide, calculer le montant pour affichage
            produit_id = form.data.get('produit')
            quantite = form.data.get('quantite')
            try:
                produit = Produit.objects.get(id=produit_id)
                prix_unitaire = produit.prix
                montant_initial = float(quantite) * float(prix_unitaire)
            except Exception:
                montant_initial = 0
            form.fields['montant'].initial = montant_initial
    else:
        form = VenteForm()
        form.fields['montant'].initial = 0
    # Préparer un dictionnaire {produit_id: prix} pour le JS
    produits_qs = Produit.objects.all()
    produits_prix = {str(p.id): float(p.prix) for p in produits_qs}
    context = {
        'form': form,
        'title': 'Enregistrer une vente',
        'produits_prix': json.dumps(produits_prix),
    }
    return render(request, 'artisans/vente_form.html', context)


@login_required
def artisan_delete(request, artisan_id):
    artisan = get_object_or_404(Artisan, id=artisan_id)
    if request.method == 'POST':
        artisan.delete()
        messages.success(request, 'Artisan supprimé avec succès.')
        return redirect('artisans:artisan_list')
    return render(request, 'artisans/confirm_delete.html', {'object': artisan, 'type': 'artisan'})

@login_required
def produit_delete(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        produit.delete()
        messages.success(request, 'Produit supprimé avec succès.')
        return redirect('artisans:produit_list')
    return render(request, 'artisans/confirm_delete.html', {'object': produit, 'type': 'produit'})

@login_required
def vente_delete(request, vente_id):
    vente = get_object_or_404(Vente, id=vente_id)
    if request.method == 'POST':
        vente.delete()
        messages.success(request, 'Vente supprimée avec succès.')
        return redirect('artisans:vente_list')
    return render(request, 'artisans/confirm_delete.html', {'object': vente, 'type': 'vente'})

@login_required
def commande_delete(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        commande.delete()
        messages.success(request, 'Commande supprimée avec succès.')
        return redirect('artisans:commande_list')
    return render(request, 'artisans/confirm_delete.html', {'object': commande, 'type': 'commande'})

# API pour les statistiques
def api_stats(request):
    """API pour les statistiques en temps réel"""
    # Statistiques générales
    total_artisans = Artisan.objects.filter(actif=True).count()
    total_produits = Produit.objects.filter(disponible=True).count()
    total_ventes = Vente.objects.filter(statut='confirmee').aggregate(total=Sum('montant'))['total'] or 0
    
    # Ventes du mois
    debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    ventes_mois = Vente.objects.filter(
        date_vente__gte=debut_mois,
        statut='confirmee'
    ).aggregate(total=Sum('montant'))['total'] or 0
    
    # Ventes par jour (7 derniers jours)
    dates = []
    ventes_par_jour = []
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        ventes_jour = Vente.objects.filter(
            date_vente__date=date,
            statut='confirmee'
        ).aggregate(total=Sum('montant'))['total'] or 0
        
        dates.append(date.strftime('%d/%m'))
        ventes_par_jour.append(float(ventes_jour))
    
    return JsonResponse({
        'total_artisans': total_artisans,
        'total_produits': total_produits,
        'total_ventes': float(total_ventes),
        'ventes_mois': float(ventes_mois),
        'ventes_par_jour': {
            'dates': list(reversed(dates)),
            'ventes': list(reversed(ventes_par_jour))
        }
    })

# Vues pour les actions AJAX
@require_POST
def update_vente_statut(request, vente_id):
    """Mettre à jour le statut d'une vente via AJAX"""
    vente = get_object_or_404(Vente, id=vente_id)
    nouveau_statut = request.POST.get('statut')
    
    if nouveau_statut in dict(Vente._meta.get_field('statut').choices):
        vente.statut = nouveau_statut
        vente.save()
        return JsonResponse({'success': True, 'statut': vente.get_statut_display()})
    
    return JsonResponse({'success': False, 'error': 'Statut invalide'})

@require_POST
def update_commande_statut(request, commande_id):
    """Mettre à jour le statut d'une commande via AJAX"""
    commande = get_object_or_404(Commande, id=commande_id)
    nouveau_statut = request.POST.get('statut')
    
    if nouveau_statut in dict(Commande._meta.get_field('statut').choices):
        commande.statut = nouveau_statut
        commande.save()
        return JsonResponse({'success': True, 'statut': commande.get_statut_display()})
    
    return JsonResponse({'success': False, 'error': 'Statut invalide'})
