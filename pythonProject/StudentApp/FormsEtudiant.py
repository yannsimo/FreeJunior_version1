from django import forms

from django.db import transaction

from .models import Student, School, Specialty, Program, Subject, Description, Photo, CV

class StudentRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="Adresse email", required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Prénom", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Nom de famille", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    study_level = forms.ChoiceField(label="Niveau d’études", choices=Student.STUDY_LEVEL_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    hourly_rate = forms.DecimalField(label="Taux horaire (€/heure)", required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Brève description de vous-même", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Décrivez-vous brièvement'}))
    photo = forms.ImageField(label="Photo de profil", required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    cv = forms.FileField(label="Curriculum Vitae (CV)", required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    school_name = forms.CharField(label="Nom de l'école où vous étudiez", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de votre école'}))
    specialty_name = forms.CharField(label="Spécialité que vous souhaitez exercer", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre spécialité'}))
    program_name = forms.CharField(label="Nom de votre filière universitaire", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de votre filière'}))
    subject_name = forms.CharField(label="Listez vos compétences ", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Listez vos  compétences'}))

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'study_level', 'hourly_rate', 'school_name', 'specialty_name', 'program_name', 'subject_name']
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom de famille',
            'email': 'Adresse email',
            'password1': 'Mot de passe',
            'password2': 'Confirmer le mot de passe',
            'study_level': 'Niveau d’études',
            'hourly_rate': 'Taux horaire (€/heure)'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'study_level': forms.Select(attrs={'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        school_name = self.cleaned_data.get('school_name')
        specialty_name = self.cleaned_data.get('specialty_name')
        program_name = self.cleaned_data.get('program_name')
        subject_name = self.cleaned_data.get('subject_name')
        description_text = self.cleaned_data.get('description')
        photo_file = self.cleaned_data.get('photo')
        cv_file = self.cleaned_data.get('cv')

        with transaction.atomic():
            school, _ = School.objects.get_or_create(name=school_name)
            specialty, _ = Specialty.objects.get_or_create(name=specialty_name)
            program, _ = Program.objects.get_or_create(name=program_name, school=school)
            subject, _ = Subject.objects.get_or_create(name=subject_name, program=program)

            student = super().save(commit=False)
            student.school = school
            student.specialty = specialty
            student.program = program
            student.related_subject = subject

            if commit:
                student.save()
                if description_text:
                    Description.objects.create(student=student, description=description_text)
                if photo_file:
                    Photo.objects.create(student=student, photo=photo_file)
                if cv_file:
                    CV.objects.create(student=student, cv=cv_file)
        return student
