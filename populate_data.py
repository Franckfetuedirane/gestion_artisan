#!/usr/bin/env python
"""
Script pour peupler la base de données avec des données de démonstration
Usage: python populate_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_artisan.settings')
django.setup()

from artisans.models import Artisan, Categorie, Produit, Vente, Commande

def create_categories():
    """Créer les catégories de produits"""
    categories_data = [
        {
            'nom': 'Poterie',
            'description': 'Objets en terre cuite et céramique',
            'icone': 'fas fa-mug-hot'
        },
        {
            'nom': 'Menuiserie',
            'description': 'Meubles et objets en bois',
            'icone': 'fas fa-tree'
        },
        {
            'nom': 'Tissage',
            'description': 'Tapis, tapisseries et textiles',
            'icone': 'fas fa-scroll'
        },
        {
            'nom': 'Métallurgie',
            'description': 'Objets en métal et ferronnerie',
            'icone': 'fas fa-hammer'
        },
        {
            'nom': 'Vannerie',
            'description': 'Objets tressés en osier et rotin',
            'icone': 'fas fa-basketball-ball'
        },
        {
            'nom': 'Bijouterie',
            'description': 'Bijoux et accessoires',
            'icone': 'fas fa-gem'
        }
    ]
    
    categories = []
    for data in categories_data:
        categorie, created = Categorie.objects.get_or_create(
            nom=data['nom'],
            defaults=data
        )
        categories.append(categorie)
        if created:
            print(f"✓ Catégorie créée : {categorie.nom}")
        else:
            print(f"→ Catégorie existante : {categorie.nom}")
    
    return categories

def create_artisans():
    """Créer les artisans"""
    artisans_data = [
        {
            'nom': 'Marie Dubois',
            'email': 'marie.dubois@email.com',
            'telephone': '+33 6 12 34 56 78',
            'adresse': '123 Rue de la Poterie\n75001 Paris',
            'specialite': 'Poterie',
            'description': 'Artisane potière depuis 15 ans, spécialisée dans la céramique traditionnelle et moderne.'
        },
        {
            'nom': 'Jean Martin',
            'email': 'jean.martin@email.com',
            'telephone': '+33 6 23 45 67 89',
            'adresse': '456 Avenue du Bois\n75002 Paris',
            'specialite': 'Menuiserie',
            'description': 'Ébéniste passionné, créateur de meubles sur mesure et d\'objets décoratifs en bois massif.'
        },
        {
            'nom': 'Fatima Benali',
            'email': 'fatima.benali@email.com',
            'telephone': '+33 6 34 56 78 90',
            'adresse': '789 Boulevard des Artisans\n75003 Paris',
            'specialite': 'Tissage',
            'description': 'Tisseuse traditionnelle, spécialisée dans les tapis berbères et les tapisseries murales.'
        },
        {
            'nom': 'Pierre Durand',
            'email': 'pierre.durand@email.com',
            'telephone': '+33 6 45 67 89 01',
            'adresse': '321 Rue de la Forge\n75004 Paris',
            'specialite': 'Métallurgie',
            'description': 'Forgeron d\'art, créateur de pièces uniques en fer forgé et d\'objets décoratifs.'
        },
        {
            'nom': 'Sophie Moreau',
            'email': 'sophie.moreau@email.com',
            'telephone': '+33 6 56 78 90 12',
            'adresse': '654 Chemin des Vanniers\n75005 Paris',
            'specialite': 'Vannerie',
            'description': 'Vannière traditionnelle, créatrice de paniers, corbeilles et objets décoratifs en osier.'
        },
        {
            'nom': 'Ahmed Hassan',
            'email': 'ahmed.hassan@email.com',
            'telephone': '+33 6 67 89 01 23',
            'adresse': '987 Place des Bijoutiers\n75006 Paris',
            'specialite': 'Bijouterie',
            'description': 'Bijoutier créateur, spécialisé dans les bijoux en argent et pierres semi-précieuses.'
        }
    ]
    
    artisans = []
    for data in artisans_data:
        artisan, created = Artisan.objects.get_or_create(
            email=data['email'],
            defaults=data
        )
        artisans.append(artisan)
        if created:
            print(f"✓ Artisan créé : {artisan.nom}")
        else:
            print(f"→ Artisan existant : {artisan.nom}")
    
    return artisans

def create_products(artisans, categories):
    """Créer les produits"""
    products_data = [
        # Poterie
        {
            'nom': 'Vase traditionnel en terre cuite',
            'description': 'Vase élégant fabriqué à la main, parfait pour les fleurs ou comme objet décoratif.',
            'prix': 45.00,
            'stock': 8,
            'materiau': 'Terre cuite',
            'dimensions': '25cm x 15cm',
            'poids': 1.2,
            'artisan_specialite': 'Poterie',
            'categorie_nom': 'Poterie'
        },
        {
            'nom': 'Set de 4 tasses en céramique',
            'description': 'Set de tasses artisanales avec motifs traditionnels, idéal pour le thé ou le café.',
            'prix': 32.00,
            'stock': 15,
            'materiau': 'Céramique',
            'dimensions': '8cm x 6cm',
            'poids': 0.8,
            'artisan_specialite': 'Poterie',
            'categorie_nom': 'Poterie'
        },
        # Menuiserie
        {
            'nom': 'Table basse en chêne massif',
            'description': 'Table basse élégante en chêne massif, finition naturelle, dimensions parfaites pour le salon.',
            'prix': 280.00,
            'stock': 3,
            'materiau': 'Chêne massif',
            'dimensions': '120cm x 60cm x 45cm',
            'poids': 25.0,
            'artisan_specialite': 'Menuiserie',
            'categorie_nom': 'Menuiserie'
        },
        {
            'nom': 'Boîte à bijoux en noyer',
            'description': 'Boîte à bijoux raffinée en noyer, avec compartiments intérieurs et fermeture magnétique.',
            'prix': 85.00,
            'stock': 12,
            'materiau': 'Noyer',
            'dimensions': '20cm x 15cm x 8cm',
            'poids': 1.5,
            'artisan_specialite': 'Menuiserie',
            'categorie_nom': 'Menuiserie'
        },
        # Tissage
        {
            'nom': 'Tapis berbère traditionnel',
            'description': 'Tapis berbère authentique, tissé à la main avec des motifs traditionnels, 100% laine naturelle.',
            'prix': 450.00,
            'stock': 2,
            'materiau': 'Laine naturelle',
            'dimensions': '200cm x 150cm',
            'poids': 8.0,
            'artisan_specialite': 'Tissage',
            'categorie_nom': 'Tissage'
        },
        {
            'nom': 'Écharpe en soie artisanale',
            'description': 'Écharpe légère en soie naturelle, tissée à la main avec des motifs géométriques élégants.',
            'prix': 75.00,
            'stock': 20,
            'materiau': 'Soie naturelle',
            'dimensions': '180cm x 30cm',
            'poids': 0.3,
            'artisan_specialite': 'Tissage',
            'categorie_nom': 'Tissage'
        },
        # Métallurgie
        {
            'nom': 'Luminaire en fer forgé',
            'description': 'Luminaire mural en fer forgé, design unique avec motifs floraux, parfait pour l\'extérieur.',
            'prix': 180.00,
            'stock': 5,
            'materiau': 'Fer forgé',
            'dimensions': '40cm x 25cm',
            'poids': 3.5,
            'artisan_specialite': 'Métallurgie',
            'categorie_nom': 'Métallurgie'
        },
        {
            'nom': 'Cendrier en cuivre martelé',
            'description': 'Cendrier élégant en cuivre martelé à la main, finition brillante, design contemporain.',
            'prix': 65.00,
            'stock': 10,
            'materiau': 'Cuivre',
            'dimensions': '12cm x 12cm x 3cm',
            'poids': 0.8,
            'artisan_specialite': 'Métallurgie',
            'categorie_nom': 'Métallurgie'
        },
        # Vannerie
        {
            'nom': 'Panier à pain en osier',
            'description': 'Panier traditionnel en osier pour le pain, tressé à la main, robuste et élégant.',
            'prix': 55.00,
            'stock': 8,
            'materiau': 'Osier',
            'dimensions': '35cm x 25cm x 15cm',
            'poids': 0.6,
            'artisan_specialite': 'Vannerie',
            'categorie_nom': 'Vannerie'
        },
        {
            'nom': 'Corbeille à fruits en rotin',
            'description': 'Corbeille à fruits élégante en rotin, design moderne, parfaite pour la décoration.',
            'prix': 42.00,
            'stock': 15,
            'materiau': 'Rotin',
            'dimensions': '30cm x 20cm x 12cm',
            'poids': 0.4,
            'artisan_specialite': 'Vannerie',
            'categorie_nom': 'Vannerie'
        },
        # Bijouterie
        {
            'nom': 'Bracelet en argent avec turquoise',
            'description': 'Bracelet élégant en argent 925, orné d\'une turquoise naturelle, fermeture à ressort.',
            'prix': 120.00,
            'stock': 25,
            'materiau': 'Argent 925',
            'dimensions': 'Taille ajustable',
            'poids': 0.1,
            'artisan_specialite': 'Bijouterie',
            'categorie_nom': 'Bijouterie'
        },
        {
            'nom': 'Bague en argent avec améthyste',
            'description': 'Bague raffinée en argent avec une améthyste naturelle, design classique et élégant.',
            'prix': 95.00,
            'stock': 18,
            'materiau': 'Argent 925',
            'dimensions': 'Tailles 50 à 60',
            'poids': 0.08,
            'artisan_specialite': 'Bijouterie',
            'categorie_nom': 'Bijouterie'
        }
    ]
    
    products = []
    for data in products_data:
        # Trouver l'artisan correspondant
        artisan = next((a for a in artisans if a.specialite == data['artisan_specialite']), artisans[0])
        # Trouver la catégorie correspondante
        categorie = next((c for c in categories if c.nom == data['categorie_nom']), categories[0])
        
        produit, created = Produit.objects.get_or_create(
            nom=data['nom'],
            artisan=artisan,
            defaults={
                'categorie': categorie,
                'description': data['description'],
                'prix': data['prix'],
                'stock': data['stock'],
                'materiau': data['materiau'],
                'dimensions': data['dimensions'],
                'poids': data['poids'],
                'disponible': True
            }
        )
        products.append(produit)
        if created:
            print(f"✓ Produit créé : {produit.nom}")
        else:
            print(f"→ Produit existant : {produit.nom}")
    
    return products

def create_sales(products):
    """Créer des ventes de démonstration"""
    clients = [
        'Marie Dupont', 'Jean Bernard', 'Sophie Martin', 'Pierre Leroy', 'Anne Moreau',
        'Michel Dubois', 'Claire Rousseau', 'François Simon', 'Isabelle Mercier',
        'Philippe Laurent', 'Nathalie Girard', 'Marc Bonnet', 'Céline Roux'
    ]
    
    modes_paiement = ['especes', 'carte', 'mobile', 'virement']
    statuts = ['confirmee', 'livree']
    
    sales = []
    for i in range(20):  # Créer 20 ventes
        produit = random.choice(products)
        quantite = random.randint(1, 3)
        prix_unitaire = produit.prix
        montant = quantite * prix_unitaire
        
        # Date aléatoire dans les 30 derniers jours
        date_vente = datetime.now() - timedelta(days=random.randint(0, 30))
        
        vente = Vente.objects.create(
            artisan=produit.artisan,
            produit=produit,
            quantite=quantite,
            prix_unitaire=prix_unitaire,
            montant=montant,
            client_nom=random.choice(clients),
            client_telephone=f"+33 6 {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}",
            client_email=f"client{random.randint(1, 100)}@email.com",
            mode_paiement=random.choice(modes_paiement),
            statut=random.choice(statuts),
            date_vente=date_vente,
            notes=f"Vente de démonstration #{i+1}"
        )
        sales.append(vente)
        print(f"✓ Vente créée : {vente.client_nom} - {produit.nom}")
    
    return sales

def create_orders(artisans):
    """Créer des commandes de démonstration"""
    clients = [
        'Hôtel Le Grand Paris', 'Restaurant La Belle Époque', 'Galerie d\'Art Moderne',
        'Boutique Élégance', 'Salon de Thé Traditionnel', 'Maison de Charme'
    ]
    
    statuts = ['nouvelle', 'en_cours', 'terminee']
    
    orders = []
    for i in range(8):  # Créer 8 commandes
        artisan = random.choice(artisans)
        date_livraison = datetime.now() + timedelta(days=random.randint(7, 60))
        
        commande = Commande.objects.create(
            artisan=artisan,
            client_nom=random.choice(clients),
            client_telephone=f"+33 1 {random.randint(40, 49)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}",
            client_email=f"commande{random.randint(1, 50)}@entreprise.com",
            description=f"Commande spéciale pour {random.choice(['décoration', 'événement', 'collection', 'exposition'])}",
            quantite=random.randint(1, 10),
            prix_estime=random.randint(100, 1000),
            date_livraison_souhaitee=date_livraison.date(),
            statut=random.choice(statuts),
            notes=f"Commande de démonstration #{i+1}"
        )
        orders.append(commande)
        print(f"✓ Commande créée : {commande.client_nom} - {artisan.nom}")
    
    return orders

def main():
    """Fonction principale"""
    print("🏺 Peuplement de la base de données Gestion Artisanale")
    print("=" * 60)
    
    # Créer les catégories
    print("\n📂 Création des catégories...")
    categories = create_categories()
    
    # Créer les artisans
    print("\n👥 Création des artisans...")
    artisans = create_artisans()
    
    # Créer les produits
    print("\n📦 Création des produits...")
    products = create_products(artisans, categories)
    
    # Créer les ventes
    print("\n💰 Création des ventes...")
    sales = create_sales(products)
    
    # Créer les commandes
    print("\n📋 Création des commandes...")
    orders = create_orders(artisans)
    
    # Résumé
    print("\n" + "=" * 60)
    print("✅ Peuplement terminé avec succès !")
    print(f"📊 Résumé :")
    print(f"   • {len(categories)} catégories")
    print(f"   • {len(artisans)} artisans")
    print(f"   • {len(products)} produits")
    print(f"   • {len(sales)} ventes")
    print(f"   • {len(orders)} commandes")
    print("\n🎉 Vous pouvez maintenant tester l'application !")
    print("   Accédez à : http://127.0.0.1:8000/")

if __name__ == '__main__':
    main() 