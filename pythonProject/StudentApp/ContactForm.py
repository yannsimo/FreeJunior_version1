from django import forms

class ContactForm(forms.Form):
    your_name = forms.CharField(max_length=100, label="Votre nom")
    your_email = forms.EmailField(label="Votre email")
    message = forms.CharField(widget=forms.Textarea, label="Votre message")
