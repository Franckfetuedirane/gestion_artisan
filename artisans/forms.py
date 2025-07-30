from django import forms
from django.forms import ModelForm
from .models import Artisan, Produit, Vente, Commande, Categorie

class ArtisanForm(ModelForm):
    class Meta:
        model = Artisan
        fields = ['nom', 'email', 'telephone', 'adresse', 'specialite', 'description', 'photo']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet de l\'artisan'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'adresse@email.com'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+33 6 12 34 56 78'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adresse complète'}),
            'specialite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Poterie, Menuiserie, Tissage...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description de l\'artisan et de son savoir-faire'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProduitForm(ModelForm):
    class Meta:
        model = Produit
        fields = ['artisan', 'categorie', 'nom', 'description', 'prix', 'stock', 'image', 'materiau', 'dimensions', 'poids', 'disponible']
        widgets = {
            'artisan': forms.Select(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description détaillée du produit'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'materiau': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Bois, Argile, Métal...'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 20cm x 15cm x 10cm'}),
            'poids': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class VenteForm(ModelForm):
    class Meta:
        model = Vente
        fields = ['artisan', 'produit', 'quantite', 'client_nom', 'client_telephone', 'client_email', 'mode_paiement', 'statut', 'notes']
        widgets = {
            'artisan': forms.Select(attrs={'class': 'form-control'}),
            'produit': forms.Select(attrs={'class': 'form-control', 'id': 'id_produit'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'id': 'id_quantite'}),
            'client_nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du client'}),
            'client_telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone du client'}),
            'client_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email du client'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notes sur la vente'}),
        }

    montant = forms.DecimalField(
        label='Montant total',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control bg-light', 'readonly': 'readonly', 'id': 'id_montant'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['montant'].initial = 0

class CommandeForm(ModelForm):
    class Meta:
        model = Commande
        fields = ['artisan', 'client_nom', 'client_telephone', 'client_email', 'description', 'quantite', 'prix_estime', 'date_livraison_souhaitee', 'statut', 'notes']
        widgets = {
            'artisan': forms.Select(attrs={'class': 'form-control'}),
            'client_nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du client'}),
            'client_telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone du client'}),
            'client_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email du client'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description détaillée de la commande'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'prix_estime': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'date_livraison_souhaitee': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notes sur la commande'}),
        }

class CategorieForm(ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'description', 'icone']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description de la catégorie'}),
            'icone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Classe CSS pour l\'icône (ex: fas fa-home)'}),
        }

class RechercheForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un artisan, produit...'
        })
    )
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(),
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    prix_min = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix minimum',
            'step': '0.01'
        })
    )
    prix_max = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix maximum',
            'step': '0.01'
        })
    ) 