# 🏺 Gestion Artisanale

Application web complète pour la gestion des artisans, de leurs produits et du suivi des ventes. Développée avec Django et Bootstrap pour offrir une interface moderne et intuitive.

## 🎯 Objectif

Cette application vise à améliorer l'organisation, la visibilité et la rentabilité des activités artisanales en remplaçant la gestion manuelle par un système informatisé complet.

## ✨ Fonctionnalités

### 👥 Gestion des Artisans
- **Enregistrement complet** : Nom, email, téléphone, adresse, spécialité
- **Profils détaillés** : Photos, descriptions, statistiques de performance
- **Recherche et filtres** : Par nom, spécialité, statut
- **Statistiques** : Total des ventes, nombre de produits, transactions

### 📦 Gestion des Produits
- **Catalogue complet** : Images, descriptions, prix, stock
- **Catégorisation** : Organisation par catégories avec icônes
- **Caractéristiques détaillées** : Matériaux, dimensions, poids
- **Gestion du stock** : Suivi des quantités disponibles

### 💰 Suivi des Ventes
- **Enregistrement des transactions** : Client, produit, quantité, prix
- **Modes de paiement** : Espèces, carte, mobile, virement
- **Statuts de vente** : En attente, confirmée, livrée, annulée
- **Historique complet** : Dates, montants, clients

### 📋 Commandes Spéciales
- **Gestion des commandes** : Description, quantité, prix estimé
- **Suivi de fabrication** : Nouvelle, en cours, terminée, livrée
- **Dates de livraison** : Planification et suivi

### 📊 Tableau de Bord
- **Statistiques en temps réel** : Artisans, produits, ventes
- **Graphiques interactifs** : Évolution des ventes, répartition par catégorie
- **Actions rapides** : Accès direct aux fonctions principales

## 🛠️ Technologies Utilisées

- **Backend** : Django 5.2.4 (Python)
- **Frontend** : Bootstrap 5.3.0, Font Awesome 6.4.0
- **Base de données** : SQLite (développement)
- **Formulaires** : Django Crispy Forms avec Bootstrap 5
- **Images** : Pillow pour le traitement des images
- **Graphiques** : Chart.js pour les visualisations

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le projet**
   ```bash
   git clone <url-du-repo>
   cd gestion_artisan
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurer la base de données**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

7. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```

8. **Accéder à l'application**
   - Interface utilisateur : http://127.0.0.1:8000/
   - Administration : http://127.0.0.1:8000/admin/

## 📁 Structure du Projet

```
gestion_artisan/
├── gestion_artisan/          # Configuration principale Django
│   ├── settings.py          # Paramètres de l'application
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # Configuration WSGI
├── artisans/                # Application principale
│   ├── models.py            # Modèles de données
│   ├── views.py             # Vues et logique métier
│   ├── forms.py             # Formulaires
│   ├── admin.py             # Interface d'administration
│   └── urls.py              # URLs de l'application
├── templates/               # Templates HTML
│   ├── base.html            # Template de base
│   └── artisans/            # Templates spécifiques
├── static/                  # Fichiers statiques
│   ├── css/                 # Styles CSS
│   ├── js/                  # JavaScript
│   └── img/                 # Images
├── media/                   # Fichiers uploadés
├── requirements.txt         # Dépendances Python
├── .gitignore              # Fichiers à ignorer
└── README.md               # Documentation
```

## 🗄️ Modèles de Données

### Artisan
- Informations personnelles (nom, email, téléphone, adresse)
- Spécialité et description
- Photo de profil
- Statut actif/inactif
- Date d'inscription

### Produit
- Nom, description, prix
- Stock disponible
- Image du produit
- Caractéristiques (matériau, dimensions, poids)
- Catégorie et artisan associé
- Statut disponible/indisponible

### Vente
- Artisan et produit concernés
- Informations client
- Quantité et montant
- Mode de paiement
- Statut de la vente
- Date et notes

### Commande
- Artisan responsable
- Description de la commande
- Informations client
- Prix estimé et quantité
- Date de livraison souhaitée
- Statut de progression

### Catégorie
- Nom et description
- Icône (classe CSS)
- Produits associés

## 🎨 Interface Utilisateur

### Design Responsive
- Interface adaptée à tous les écrans
- Navigation intuitive
- Cartes et tableaux modernes
- Animations et transitions fluides

### Couleurs et Thème
- Palette de couleurs professionnelle
- Gradients et ombres pour la profondeur
- Icônes Font Awesome
- Typographie Poppins

### Composants
- **Cartes statistiques** : Affichage des métriques importantes
- **Formulaires stylisés** : Validation et feedback visuel
- **Tableaux interactifs** : Tri, filtrage, pagination
- **Modales et alertes** : Notifications et confirmations

## 🔧 Configuration

### Variables d'environnement
```python
# settings.py
DEBUG = True  # False en production
SECRET_KEY = 'votre-clé-secrète'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Fichiers média
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Personnalisation
- Modifier les couleurs dans `static/css/style.css`
- Ajouter des catégories via l'interface d'administration
- Configurer les permissions utilisateur
- Personnaliser les templates selon vos besoins

## 📱 Fonctionnalités Avancées

### API REST
- Endpoints pour les statistiques
- Mise à jour des statuts via AJAX
- Export de données

### Recherche et Filtres
- Recherche textuelle en temps réel
- Filtres par catégorie, prix, artisan
- Pagination intelligente

### Notifications
- Messages de succès/erreur
- Alertes auto-fermantes
- Notifications toast

### Export et Impression
- Export CSV des données
- Impression des rapports
- Génération de factures

## 🔒 Sécurité

- Authentification Django
- Protection CSRF
- Validation des formulaires
- Gestion des permissions
- Sanitisation des données

## 🚀 Déploiement

### Production
1. Configurer une base de données PostgreSQL
2. Collecter les fichiers statiques : `python manage.py collectstatic`
3. Configurer un serveur web (Nginx + Gunicorn)
4. Définir `DEBUG = False`
5. Configurer les variables d'environnement

### Docker (optionnel)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Contacter l'équipe de développement
- Consulter la documentation Django

## 🎉 Remerciements

- Django pour le framework web
- Bootstrap pour l'interface utilisateur
- Font Awesome pour les icônes
- Chart.js pour les graphiques
- La communauté open source

---

**Développé avec ❤️ pour valoriser l'artisanat local** 