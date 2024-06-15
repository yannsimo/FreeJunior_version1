from django import forms
from django.core.exceptions import ValidationError
from .models import Company

class EntrepriseRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email', 'contact_info']
        labels = {
            'name': "Entrez le nom de l'entreprise",
            'email': "Entrez l'adresse email de l'entreprise",
            'contact_info': "Entrez le numéro de téléphone de l'entreprise",
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Company.objects.filter(email=email).exists():
            raise ValidationError("Une entreprise avec cet email existe déjà.")
        return email

    def clean_contact_info(self):
        contact_info = self.cleaned_data.get('contact_info')
        if not contact_info.isdigit():
            raise ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")
        return contact_info
