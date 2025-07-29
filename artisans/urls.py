from django.urls import path
from . import views

app_name = 'artisans'

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    
    # Artisans
    path('artisans/', views.artisan_list, name='artisan_list'),
    path('artisans/<uuid:artisan_id>/', views.artisan_detail, name='artisan_detail'),
    path('artisans/ajouter/', views.artisan_create, name='artisan_create'),
    path('artisans/<uuid:artisan_id>/modifier/', views.artisan_update, name='artisan_update'),
    path('artisans/<uuid:artisan_id>/supprimer/', views.artisan_delete, name='artisan_delete'),
    
    # Produits
    path('produits/', views.produit_list, name='produit_list'),
    path('produits/<uuid:produit_id>/', views.produit_detail, name='produit_detail'),
    path('produits/ajouter/', views.produit_create, name='produit_create'),
    path('produits/<uuid:produit_id>/modifier/', views.produit_update, name='produit_update'),
    path('produits/<uuid:produit_id>/supprimer/', views.produit_delete, name='produit_delete'),
    
    # Ventes
    path('ventes/', views.vente_list, name='vente_list'),
    path('ventes/<uuid:vente_id>/', views.vente_detail, name='vente_detail'),
    path('ventes/ajouter/', views.vente_create, name='vente_create'),
    path('ventes/<uuid:vente_id>/supprimer/', views.vente_delete, name='vente_delete'),
    
    # Commandes
    path('commandes/', views.commande_list, name='commande_list'),
    path('commandes/ajouter/', views.commande_create, name='commande_create'),
    path('commandes/<uuid:commande_id>/supprimer/', views.commande_delete, name='commande_delete'),
    
    # API
    path('api/stats/', views.api_stats, name='api_stats'),
    path('api/ventes/<uuid:vente_id>/statut/', views.update_vente_statut, name='update_vente_statut'),
    path('api/commandes/<uuid:commande_id>/statut/', views.update_commande_statut, name='update_commande_statut'),
] 