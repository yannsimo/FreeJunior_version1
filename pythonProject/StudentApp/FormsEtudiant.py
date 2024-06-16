from unittest import TestCase
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
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
    ('ux_ui_Design', 'UX/UI Design'),
    ('big_data', 'Big Data'),
    ('realite_virtuelle', 'Réalité Virtuelle / Réalité Augmentée'),
    ('robotique', 'Robotique'),
    ('ingenierie_logicielle', 'Ingénierie Logicielle'),
    ('systemes_embarques', 'Systèmes Embarqués'),
    ('automatisation', 'Automatisation'),
    ('conception_base_de_donnees', 'Conception de Bases de Données'),
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
    description = forms.CharField(
        label="Brève description de vous-même",
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': (
                "Décrivez-vous brièvement. Voici quelques points à inclure pour atteindre les 300 mots : \n"
                "- Qui êtes-vous et quel est votre parcours académique ? \n"
                "- Quelles sont les stages que vous avez effectués ? \n"
                "- Sur quels projets avez-vous travaillé ? \n"
                "- Quelles compétences techniques maîtrisez-vous ? \n"
                "- Quelles sont vos compétences personnelles et vos forces ? \n"
                "- Quels sont vos objectifs professionnels ? \n"
                "- Quelles sont vos réalisations notables ? \n"
            )
        })
    )
    photo = forms.ImageField(label="Photo de profil", required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    cv = forms.FileField(label="Curriculum Vitae (CV)", required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    school_name = forms.CharField(label="Nom de l'école où vous étudiez", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de votre école'}))
    specialty_name = forms.ChoiceField(
        label="Spécialité que vous souhaitez exercer sur ce site ",
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

    def clean_description(self):
        description_text = self.cleaned_data.get('description')
        word_count = len(description_text.split())
        if word_count < 100:
            raise ValidationError('La description doit contenir au moins 100 mots.')
        return description_text

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

class StudentRegistrationFormTests(TestCase):

    def setUp(self):
        self.school = School.objects.create(name="Test School")
        self.specialty = Specialty.objects.create(name="Développement Web")
        self.program = Program.objects.create(name="Test Program", school=self.school)
        self.subject = Subject.objects.create(name="Test Subject", program=self.program)
        self.valid_data = {
            'email': 'teststudent@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'study_level': 'Bac+3',
            'hourly_rate': '20.00',
            'description': 'Je suis un étudiant en développement web avec une passion pour les nouvelles technologies et l\'apprentissage continu. J\'ai effectué plusieurs stages dans des entreprises de renom, travaillant sur des projets variés allant de la conception de sites web à la gestion de bases de données. Je maîtrise HTML, CSS, JavaScript, et divers frameworks tels que React et Angular. Mes compétences en communication et en gestion de projet m\'ont permis de collaborer efficacement avec des équipes pluridisciplinaires. Mon objectif est de devenir un développeur full-stack compétent et de contribuer à des projets innovants. Mes réalisations incluent la création d\'applications web interactives et la participation à des hackathons où j\'ai gagné des prix. Je suis motivé, déterminé, et toujours prêt à relever de nouveaux défis.',
            'photo': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            'cv': SimpleUploadedFile(name='test_cv.pdf', content=b'', content_type='application/pdf'),
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'school_name': self.school.name,
            'specialty_name': self.specialty.name,
            'program_name': self.program.name,
            'subject_name': self.subject.name,
        }

    def test_student_registration_form_valid(self):
        form = StudentRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        student = form.save()
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(student.first_name, 'John')
        self.assertEqual(student.last_name, 'Doe')
        self.assertEqual(student.email, 'teststudent@example.com')

    def test_student_registration_form_invalid_password_mismatch(self):
        self.valid_data['password2'] = 'differentpassword'
        form = StudentRegistrationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_student_registration_form_invalid_short_description(self):
        self.valid_data['description'] = 'Trop court.'
        form = StudentRegistrationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_student_registration_form_save_description(self):
        form = StudentRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        student = form.save()
        self.assertEqual(Description.objects.count(), 1)
        self.assertEqual(student.student_description.description, self.valid_data['description'])

    def test_student_registration_form_save_photo(self):
        form = StudentRegistrationForm(data=self.valid_data, files={'photo': self.valid_data['photo']})
        self.assertTrue(form.is_valid())
        student = form.save()
        self.assertEqual(Photo.objects.count(), 1)
        self.assertEqual(student.student_photo.photo.name, 'student_photos/test_image.jpg')

    def test_student_registration_form_save_cv(self):
        form = StudentRegistrationForm(data=self.valid_data, files={'cv': self.valid_data['cv']})
        self.assertTrue(form.is_valid())
        student = form.save()
        self.assertEqual(CV.objects.count(), 1)
        self.assertEqual(student.student_cv.cv.name, 'student_cvs/test_cv.pdf')

    def test_student_update(self):
        form = StudentRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        student = form.save()

        updated_data = self.valid_data.copy()
        updated_data['first_name'] = 'Jane'
        updated_data['description'] = 'Je suis un étudiant en développement web avec une passion renouvelée pour les nouvelles technologies et l\'apprentissage continu. J\'ai effectué plusieurs stages dans des entreprises de renom, travaillant sur des projets variés allant de la conception de sites web à la gestion de bases de données. Je maîtrise HTML, CSS, JavaScript, et divers frameworks tels que React et Angular. Mes compétences en communication et en gestion de projet m\'ont permis de collaborer efficacement avec des équipes pluridisciplinaires. Mon objectif est de devenir un développeur full-stack compétent et de contribuer à des projets innovants. Mes réalisations incluent la création d\'applications web interactives et la participation à des hackathons où j\'ai gagné des prix. Je suis motivé, déterminé, et toujours prêt à relever de nouveaux défis.'

        form = StudentRegistrationForm(data=updated_data, instance=student)
        self.assertTrue(form.is_valid())
        updated_student = form.save()
        self.assertEqual(updated_student.first_name, 'Jane')
        self.assertEqual(updated_student.student_description.description, updated_data['description'])

    def test_student_deletion(self):
        form = StudentRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        student = form.save()

        student_id = student.id
        student.delete()
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(id=student_id)
