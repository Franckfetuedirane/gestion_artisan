from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

class Artisan(models.Model):
    """Modèle pour représenter un artisan"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(unique=True, verbose_name="Adresse email")
    telephone = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    adresse = models.TextField(verbose_name="Adresse")
    specialite = models.CharField(max_length=100, verbose_name="Spécialité")
    description = models.TextField(blank=True, verbose_name="Description")
    photo = models.ImageField(upload_to='artisans/', blank=True, null=True, verbose_name="Photo de profil")
    date_inscription = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    actif = models.BooleanField(default=True, verbose_name="Artisan actif")
    
    class Meta:
        verbose_name = "Artisan"
        verbose_name_plural = "Artisans"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    @property
    def total_ventes(self):
        """Calculer le total des ventes de l'artisan"""
        return sum(vente.montant for vente in self.ventes.all())
    
    @property
    def nombre_produits(self):
        """Compter le nombre de produits de l'artisan"""
        return self.produits.count()

class Categorie(models.Model):
    """Modèle pour les catégories de produits"""
    nom = models.CharField(max_length=50, unique=True, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, verbose_name="Description")
    icone = models.CharField(max_length=50, blank=True, verbose_name="Icône (classe CSS)")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class Produit(models.Model):
    """Modèle pour représenter un produit artisanal"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE, related_name='produits', verbose_name="Artisan")
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name='produits', verbose_name="Catégorie")
    nom = models.CharField(max_length=200, verbose_name="Nom du produit")
    description = models.TextField(verbose_name="Description")
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    image = models.ImageField(upload_to='produits/', blank=True, null=True, verbose_name="Image du produit")
    materiau = models.CharField(max_length=100, blank=True, verbose_name="Matériau principal")
    dimensions = models.CharField(max_length=100, blank=True, verbose_name="Dimensions")
    poids = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Poids (kg)")
    disponible = models.BooleanField(default=True, verbose_name="Produit disponible")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.nom} - {self.artisan.nom}"
    
    @property
    def total_ventes(self):
        """Calculer le total des ventes de ce produit"""
        return sum(vente.montant for vente in self.ventes.all())

class Vente(models.Model):
    """Modèle pour enregistrer les ventes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE, related_name='ventes', verbose_name="Artisan")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='ventes', verbose_name="Produit")
    quantite = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")
    client_nom = models.CharField(max_length=100, verbose_name="Nom du client")
    client_telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone du client")
    client_email = models.EmailField(blank=True, verbose_name="Email du client")
    mode_paiement = models.CharField(
        max_length=20,
        choices=[
            ('especes', 'Espèces'),
            ('carte', 'Carte bancaire'),
            ('mobile', 'Paiement mobile'),
            ('virement', 'Virement bancaire'),
        ],
        default='especes',
        verbose_name="Mode de paiement"
    )
    statut = models.CharField(
        max_length=20,
        choices=[
            ('en_attente', 'En attente'),
            ('confirmee', 'Confirmée'),
            ('livree', 'Livrée'),
            ('annulee', 'Annulée'),
        ],
        default='en_attente',
        verbose_name="Statut de la vente"
    )
    date_vente = models.DateTimeField(auto_now_add=True, verbose_name="Date de vente")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ['-date_vente']
    
    def __str__(self):
        return f"Vente {self.id} - {self.produit.nom} - {self.artisan.nom}"
    
    def save(self, *args, **kwargs):
        # Calculer automatiquement le montant total
        if not self.montant:
            self.montant = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)

class Commande(models.Model):
    """Modèle pour les commandes spéciales"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE, related_name='commandes', verbose_name="Artisan")
    client_nom = models.CharField(max_length=100, verbose_name="Nom du client")
    client_telephone = models.CharField(max_length=20, verbose_name="Téléphone du client")
    client_email = models.EmailField(blank=True, verbose_name="Email du client")
    description = models.TextField(verbose_name="Description de la commande")
    quantite = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    prix_estime = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix estimé")
    date_commande = models.DateTimeField(auto_now_add=True, verbose_name="Date de commande")
    date_livraison_souhaitee = models.DateField(verbose_name="Date de livraison souhaitée")
    statut = models.CharField(
        max_length=20,
        choices=[
            ('nouvelle', 'Nouvelle'),
            ('en_cours', 'En cours de fabrication'),
            ('terminee', 'Terminée'),
            ('livree', 'Livrée'),
            ('annulee', 'Annulée'),
        ],
        default='nouvelle',
        verbose_name="Statut de la commande"
    )
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-date_commande']
    
    def __str__(self):
        return f"Commande {self.id} - {self.client_nom} - {self.artisan.nom}"
