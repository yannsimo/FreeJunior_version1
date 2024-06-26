
from unittest import TestCase
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.template.defaultfilters import slugify, date
from django.contrib.auth  import get_user_model
User = get_user_model()


SPECIALTY_CHOICES = [
    ('developpement_web', 'Développement Web'),
    ('design_graphique', 'Design Graphique'),
    ('data_science', 'Data Science'),
    ('marketing', 'Marketing'),
    ('blockchain', 'Blockchain'),
    ('recherche_et_developpement', 'Recherche et Développement'),
    ('iot', 'Internet des Objets (IoT)'),
    ('ux_ui_Design', 'UX/UI Design'),
    ('big_data', 'Big Data'),
    ('audiovisual_production', 'Production Audiovisuelle')
]
PAYMENT_CHOICES = [
    ('cash', 'Cash'),
    ('equity', 'Parts d\'entreprise'),
]

class School(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Specialty(models.Model):
    name = models.CharField(max_length=100)
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.get_human_readable_name()

    def get_human_readable_name(self):
        return dict(SPECIALTY_CHOICES).get(self.name,  self.name)

class Program(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='programs')

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class Student(models.Model):
    STUDY_LEVEL_CHOICES = [
        ('Bac+3', 'Bac+3'),
        ('Bac+4', 'Bac+4'),
        ('Bac+5', 'Bac+5'),
        ('Bac+6', 'Bac+6'),
        ('Bac+7', 'Bac+7'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    study_level = models.CharField(max_length=5, choices=STUDY_LEVEL_CHOICES, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students', null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='students', null=True)
    related_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    description = models.TextField(null=True)
    photo = models.ImageField(upload_to='student_photos/', null=True)
    cv = models.FileField(upload_to='student_cvs/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True)
    contact_info = models.TextField()
    def __str__(self):
        return self.name



class Mission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True,default=None)  # Définit l'étudiant par défaut à None
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='missions')
    specialty= models.ForeignKey(Specialty, on_delete=models.CASCADE, null=True)
    payment_type = models.CharField(max_length=6, choices=PAYMENT_CHOICES,null=True)
    cash_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    equity_offer = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.payment_type == 'cash':
            self.equity_offer = None
        elif self.payment_type == 'equity':
            self.cash_amount = None
        super().save(*args, **kwargs)
class Comment(models.Model):
    STATUS_VISIBLE = 'visible'
    STATUS_HIDDEN = 'hidden'
    STATUS_MODERATED = 'moderated'

    STATUS_CHOICES = (
        (STATUS_VISIBLE, 'Visible'),
        (STATUS_HIDDEN, 'Hidden'),
        (STATUS_MODERATED, 'Moderated'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='comments')
    company_name = models.CharField(max_length=100)
    mission_title = models.CharField(max_length=100)
    text = models.TextField()
    status = models.CharField(max_length=20, default=STATUS_VISIBLE, choices=STATUS_CHOICES)
    moderation_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {} (status={})'.format(self.company_name, self.text[:20], self.status)

