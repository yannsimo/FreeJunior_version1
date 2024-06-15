"""
URL configuration for FreeJunior_version1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from StudentApp import  views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('page_company/', views.page_company, name='page_company'),
    path('confirmationMessage/',views.confirmationMessage, name='confirmationMessage'),
    path('confirmationInscription/', views.confirmationInscription, name ='confirmationInscription'),
    path('confirmationEntreprise/', views.confirmationEntreprise, name ='confirmationEntreprise'),
    path('Accueil/', views.Pageaccueil,name='accueil'),
    path('page_etudiant/', views.page_etudiant, name='page_etudiant'),
    path('FormulaireEtudiant/', views.register_student, name='student_form'),
    path('FormulaireEntreprise/', views.register_company, name='company_form'),
    path('Etudiants/', views.student_list, name='student_list'),
    path('detail/<int:student_id>/', views.student_detail,name='student_detail'),
    path('Etudiants/<str:speciality_name>/', views.student_list, name='student_list_filter'),
    path('student/<int:student_id>/contact/', views.student_detail, name='contact_student'),
    path('etudiant/<int:pk>/modifier/', views.edit_student_profile, name='edit_student_profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
