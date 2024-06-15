from django.urls import reverse

from django.http import HttpRequest

from .FormsEtudiant import StudentRegistrationForm
from .FormsEntreprise import EntrepriseRegistrationForm
from .ContactForm import ContactForm
from StudentApp import navigation, model_helpers

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from StudentApp.models import Student , Comment
from django.core.mail import send_mail
from .CommentForm import CreateComment

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.instance)
            return redirect('confirmationInscription')
    else:
        form = StudentRegistrationForm()

    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_FormStudent),
        'form': form
    }

    return render(request, 'StudentApp/student_form.html', context)

def register_company(request):
    if request.method == 'POST':
        form = EntrepriseRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('confirmationEntreprise')
    else:
        form = EntrepriseRegistrationForm()

    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_FormCompany),
        'form': form
    }
    return render(request, 'StudentApp/Entreprise_form.html', context)

def student_list(request, speciality_name=model_helpers.student_speciality_all.slug()):
    speciality, students = model_helpers.get_speciality_Student(speciality_name)
    specialities = model_helpers.get_speciality()
    context = {
        'specialities': specialities,
        'students': students,
        'speciality': speciality,
        'navigation_items': navigation.navigation_items(navigation.NAV_FormListStudent),
    }
    return render(request, 'StudentApp/student_list.html', context)
def edit_student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentRegistrationForm(instance=student)

    context = {
        'form': form,
        'student': student
    }
    return render(request, 'StudentApp/edit_student_profile.html', context)


def page_company(request):
    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_FormCompany),
    }
    return render(request, 'StudentApp/PageEntreprise.html', context)


def page_etudiant(request):
    context = {
        'navigation_items':  navigation.navigation_items(navigation.NAV_FormStudent),
    }
    return render(request, 'StudentApp/PageEtudiant.html', context)


def confirmationInscription(request):

    return render(request, 'StudentApp/ConfirmationIncription.html')
def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    comments = student.comments.exclude(status=Comment.STATUS_HIDDEN).order_by('created_at')

    if request.method == 'POST':
        comment_form = CreateComment(request.POST)
        form = ContactForm(request.POST)

        if form.is_valid():
            your_name = form.cleaned_data['your_name']
            your_email = form.cleaned_data['your_email']
            message = form.cleaned_data['message']
            subject = f"Message de {your_name} via FreeJunior"
            email_message = f"De: {your_name}\nEmail: {your_email}\n\nMessage:\n{message}"
            try:
                send_mail(subject, email_message, your_email, [student.email])
                messages.success(request, "Votre message a été envoyé.")
                return redirect(f"{reverse('confirmationMessage')}?name={your_name}&email={your_email}&student_name={student.first_name}")
            except Exception as e:
                messages.error(request, "Une erreur s'est produite lors de l'envoi de l'email.")

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.student = student
            comment.save()
            messages.success(request, "Votre commentaire a été ajouté avec succès.")
    else:
        comment_form = CreateComment()
        form = ContactForm()

    context = {
        'student': student,
        'form': form,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'StudentApp/student_detail.html', context)


def confirmationMessage(request):
    name = request.GET.get('name')
    email = request.GET.get('email')
    student_name = request.GET.get('student_name')
    context = {
        'name': name,
        'email': email,
        'student_name':student_name,
    }
    return render(request, 'StudentApp/ConfirmationMessage.html', context)


def confirmationEntreprise(request):
    return render(request, 'StudentApp/ConfirmationEntreprise.html')

def Pageaccueil(request):
    return render(request, 'StudentApp/Accueil.html')
