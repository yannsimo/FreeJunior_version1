from django import forms

from django.db import transaction

from .models import Student, School, Specialty, Program, Subject, Description, Photo, CV

SPECIALTY_CHOICES = [
    ('developpement_web', 'Développement Web'),
    ('design_graphique', 'Design Graphique'),
    ('data_science', 'Data Science'),
    ('marketing', 'Marketing'),
    ('redaction', 'Rédaction'),
    ('developpement_mobile', 'Développement Mobile'),
    ('cybersecurite', 'Cybersécurité'),
    ('intelligence_artificielle', 'Intelligence Artificielle'),
    ('reseau', 'Réseaux et Télécommunications'),
    ('administration_systeme', 'Administration Système'),
    ('gestion_projet', 'Gestion de Projet'),
    ('cloud_computing', 'Cloud Computing'),
    ('devops', 'DevOps'),
    ('test_qualite', 'Test et Assurance Qualité'),
    ('analyse_donnees', 'Analyse de Données'),
    ('consultant_informatique', 'Consultant Informatique'),
    ('architecte_logiciel', 'Architecte Logiciel'),
    ('support_technique', 'Support Technique'),
    ('machine_learning', 'Machine Learning'),
    ('blockchain', 'Blockchain'),
    ('recherche_et_developpement', 'Recherche et Développement'),
    ('iot', 'Internet des Objets (IoT)'),
    ('ux_ui', 'UX/UI Design'),
    ('big_data', 'Big Data'),
    ('realite_virtuelle', 'Réalité Virtuelle / Réalité Augmentée'),
    ('robotique', 'Robotique'),
    ('ingenierie_logicielle', 'Ingénierie Logicielle'),
    ('systemes_embarques', 'Systèmes Embarqués'),
    ('automatisation', 'Automatisation'),
    ('conception_bdd', 'Conception de Bases de Données'),
    ('administration_reseaux', 'Administration Réseaux'),
    ('virtualisation', 'Virtualisation'),
    ('ingenieur_systeme', 'Ingénieur Système'),
    ('developpement_jeux_video', 'Développement de Jeux Vidéo'),
    ('bi_informatique', 'BI (Business Intelligence)'),
    ('securite_informatique', 'Sécurité Informatique'),
    ('telecommunications', 'Télécommunications'),
    ('integration_systemes', 'Intégration de Systèmes'),
    ('maintenance_informatique', 'Maintenance Informatique'),
    ('gestion_reseaux', 'Gestion des Réseaux'),
    ('ingenierie_informatique', 'Ingénierie Informatique'),
    ('infographie', 'Infographie'),
    ('seo_sem', 'SEO/SEM (Référencement)'),
    ('gestion_contenu', 'Gestion de Contenu'),
    ('formation_informatique', 'Formation Informatique'),
    ('e-commerce', 'E-commerce'),
    ('copywriting', 'Copywriting'),
    ('traduction', 'Traduction'),
    ('support_client', 'Support Client'),
    ('video_montage', 'Montage Vidéo'),
    ('photographie', 'Photographie'),
    ('community_management', 'Community Management'),
    ('gestion_reseaux_sociaux', 'Gestion des Réseaux Sociaux'),
    ('animation_2d_3d', 'Animation 2D/3D'),
    ('illustration', 'Illustration'),
    ('brand_identity', 'Identité de Marque'),
    ('production_podcast', 'Production de Podcast'),
    ('mise_en_page', 'Mise en Page'),
    ('consultant_seo', 'Consultant SEO'),
    ('conception_email_marketing', 'Conception Email Marketing'),
    ('relations_publiques', 'Relations Publiques'),
    ('gestion_evenements', 'Gestion d\'Événements'),
    ('stratégie_de_marque', 'Stratégie de Marque'),
    ('voice_over', 'Voice Over'),
    ('scriptwriting', 'Écriture de Scénarios'),
    ('chatbot_development', 'Développement de Chatbots'),
    ('proofreading', 'Relecture et Correction'),
    ('financial_analysis', 'Analyse Financière'),
    ('data_entry', 'Saisie de Données'),
    ('virtual_assistant', 'Assistant Virtuel'),
    ('market_research', 'Études de Marché'),
    ('social_media_ads', 'Publicités sur les Réseaux Sociaux'),
    ('content_creation', 'Création de Contenu'),
    ('email_campaign_management', 'Gestion des Campagnes Email'),
    ('affiliate_marketing', 'Marketing d\'Affiliation'),
    ('product_management', 'Gestion de Produit'),
    ('growth_hacking', 'Growth Hacking'),
    ('user_research', 'Recherche Utilisateur'),
    ('content_strategy', 'Stratégie de Contenu'),
    ('digital_strategy', 'Stratégie Digitale'),
    ('excel', 'Maîtrise d\'Excel'),
    ('power_bi', 'Power BI'),
    ('tableau', 'Tableau'),
    ('sap', 'SAP'),
    ('oracle', 'Oracle'),
    ('sas', 'SAS'),
    ('sql', 'SQL'),
    ('nosql', 'NoSQL'),
    ('network_security', 'Sécurité Réseau'),
    ('ethical_hacking', 'Ethical Hacking'),
    ('pen_testing', 'Pen Testing'),
    ('salesforce', 'Salesforce'),
    ('crm_implementation', 'Implémentation CRM'),
    ('technical_support', 'Support Technique'),
    ('helpdesk_support', 'Support Helpdesk'),
    ('it_consulting', 'Consulting IT'),
    ('virtual_event_planning', 'Organisation d\'Événements Virtuels'),
    ('online_tutoring', 'Tutorat en Ligne'),
    ('web_analytics', 'Web Analytics'),
    ('adobe_creative_suite', 'Adobe Creative Suite'),
    ('final_cut_pro', 'Final Cut Pro'),
    ('adobe_premiere_pro', 'Adobe Premiere Pro'),
    ('music_production', 'Production Musicale'),
    ('game_testing', 'Test de Jeux Vidéo'),
    ('qa_testing', 'Test QA'),
    ('mobile_app_design', 'Design d\'Applications Mobiles'),
    ('3d_modeling', 'Modélisation 3D'),
    ('vr_ar_development', 'Développement VR/AR'),
    ('game_development', 'Développement de Jeux Vidéo'),
    ('app_store_optimization', 'Optimisation App Store'),
    ('hr_consulting', 'Consulting RH'),
    ('legal_consulting', 'Consulting Juridique'),
    ('financial_modeling', 'Modélisation Financière'),
    ('accounting', 'Comptabilité'),
    ('tax_preparation', 'Préparation Fiscale'),
    ('business_plan_writing', 'Rédaction de Business Plan'),
    ('project_management', 'Gestion de Projet'),
    ('agile_scrum', 'Agile/Scrum'),
    ('kanban', 'Kanban'),
    ('lean_methodology', 'Méthodologie Lean'),
    ('supply_chain_management', 'Gestion de la Chaîne d\'Approvisionnement'),
    ('logistics', 'Logistique'),
    ('inventory_management', 'Gestion des Stocks'),
    ('procurement', 'Approvisionnement'),
    ('vendor_management', 'Gestion des Fournisseurs'),
    ('erp_implementation', 'Implémentation ERP'),
    ('business_process_improvement', 'Amélioration des Processus Business'),
    ('technical_writing', 'Rédaction Technique'),
    ('content_editing', 'Édition de Contenu'),
    ('ux_research', 'Recherche UX'),
    ('information_architecture', 'Architecture de l\'Information'),
    ('interaction_design', 'Design d\'Interaction'),
    ('prototyping', 'Prototypage'),
    ('usability_testing', 'Test d\'Utilisabilité'),
    ('responsive_design', 'Design Responsive'),
    ('web_design', 'Design Web'),
    ('graphic_design', 'Design Graphique'),
    ('logo_design', 'Design de Logo'),
    ('brand_identity_design', 'Design d\'Identité de Marque'),
    ('print_design', 'Design Print'),
    ('package_design', 'Design d\'Emballage'),
    ('motion_graphics', 'Motion Graphics'),
    ('illustration', 'Illustration'),
    ('infographics', 'Infographies'),
    ('presentation_design', 'Design de Présentations'),
    ('brochure_design', 'Design de Brochures'),
    ('business_card_design', 'Design de Cartes de Visite'),
    ('flyer_design', 'Design de Flyers'),
    ('menu_design', 'Design de Menus'),
    ('poster_design', 'Design de Posters'),
    ('book_cover_design', 'Design de Couvertures de Livre'),
    ('album_cover_design', 'Design de Couvertures d\'Album'),
    ('t_shirt_design', 'Design de T-shirts'),
    ('fashion_design', 'Design de Mode'),
    ('jewelry_design', 'Design de Bijoux'),
    ('product_design', 'Design de Produits'),
    ('industrial_design', 'Design Industriel'),
    ('interior_design', 'Design d\'Intérieur'),
    ('landscape_design', 'Design Paysager'),
    ('architecture_design', 'Design Architectural'),
    ('home_staging', 'Home Staging'),
    ('real_estate_photography', 'Photographie Immobilière'),
    ('aerial_photography', 'Photographie Aérienne'),
    ('event_photography', 'Photographie d\'Événements'),
    ('portrait_photography', 'Photographie de Portrait'),
    ('audiovisual_production', 'Production Audiovisuelle')]
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
    specialty_name = forms.ChoiceField(
        label="Spécialité que vous souhaitez exercer",
        choices=SPECIALTY_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
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
