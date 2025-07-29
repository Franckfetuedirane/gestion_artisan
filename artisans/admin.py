from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Artisan, Categorie, Produit, Vente, Commande

@admin.register(Artisan)
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ['nom', 'specialite', 'telephone', 'email', 'actif', 'total_ventes_display', 'nombre_produits_display', 'date_inscription']
    list_filter = ['actif', 'specialite', 'date_inscription']
    search_fields = ['nom', 'email', 'telephone', 'specialite']
    readonly_fields = ['date_inscription', 'total_ventes_display', 'nombre_produits_display']
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'email', 'telephone', 'adresse', 'photo')
        }),
        ('Informations professionnelles', {
            'fields': ('specialite', 'description', 'actif')
        }),
        ('Statistiques', {
            'fields': ('total_ventes_display', 'nombre_produits_display', 'date_inscription'),
            'classes': ('collapse',)
        }),
    )
    
    def total_ventes_display(self, obj):
        return f"{obj.total_ventes:.2f} €"
    total_ventes_display.short_description = "Total des ventes"
    
    def nombre_produits_display(self, obj):
        return obj.nombre_produits
    nombre_produits_display.short_description = "Nombre de produits"

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'nombre_produits', 'icone']
    search_fields = ['nom']
    
    def nombre_produits(self, obj):
        return obj.produits.count()
    nombre_produits.short_description = "Nombre de produits"

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'artisan', 'categorie', 'prix', 'stock', 'disponible', 'total_ventes_display', 'date_creation']
    list_filter = ['disponible', 'categorie', 'artisan', 'date_creation']
    search_fields = ['nom', 'artisan__nom', 'description']
    readonly_fields = ['date_creation', 'date_modification', 'total_ventes_display']
    fieldsets = (
        ('Informations générales', {
            'fields': ('artisan', 'categorie', 'nom', 'description', 'image')
        }),
        ('Prix et stock', {
            'fields': ('prix', 'stock', 'disponible')
        }),
        ('Caractéristiques', {
            'fields': ('materiau', 'dimensions', 'poids'),
            'classes': ('collapse',)
        }),
        ('Statistiques', {
            'fields': ('total_ventes_display', 'date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def total_ventes_display(self, obj):
        return f"{obj.total_ventes:.2f} €"
    total_ventes_display.short_description = "Total des ventes"

@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    list_display = ['id', 'artisan', 'produit', 'quantite', 'montant', 'client_nom', 'statut', 'date_vente']
    list_filter = ['statut', 'mode_paiement', 'date_vente', 'artisan']
    search_fields = ['client_nom', 'artisan__nom', 'produit__nom']
    readonly_fields = ['date_vente', 'montant']
    fieldsets = (
        ('Informations de vente', {
            'fields': ('artisan', 'produit', 'quantite', 'prix_unitaire', 'montant')
        }),
        ('Informations client', {
            'fields': ('client_nom', 'client_telephone', 'client_email')
        }),
        ('Détails de la transaction', {
            'fields': ('mode_paiement', 'statut', 'notes')
        }),
        ('Date', {
            'fields': ('date_vente',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Calculer automatiquement le montant si pas déjà fait
        if not obj.montant:
            obj.montant = obj.quantite * obj.prix_unitaire
        super().save_model(request, obj, form, change)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'artisan', 'client_nom', 'quantite', 'prix_estime', 'statut', 'date_commande', 'date_livraison_souhaitee']
    list_filter = ['statut', 'date_commande', 'artisan']
    search_fields = ['client_nom', 'artisan__nom', 'description']
    readonly_fields = ['date_commande']
    fieldsets = (
        ('Informations de commande', {
            'fields': ('artisan', 'description', 'quantite', 'prix_estime')
        }),
        ('Informations client', {
            'fields': ('client_nom', 'client_telephone', 'client_email')
        }),
        ('Suivi', {
            'fields': ('statut', 'date_livraison_souhaitee', 'notes')
        }),
        ('Date', {
            'fields': ('date_commande',),
            'classes': ('collapse',)
        }),
    )
