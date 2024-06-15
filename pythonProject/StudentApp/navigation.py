from django.urls import reverse_lazy

NAV_FormStudent = 'Etudiant'
NAV_FormCompany = 'Entreprise'
NAV_FormListStudent = 'Liste des etudiants '
NAV_ITEMS = [
    (NAV_FormStudent, reverse_lazy('page_etudiant')),
    (NAV_FormCompany, reverse_lazy('page_company')),
    (NAV_FormListStudent, reverse_lazy('student_list')),
]

def navigation_items(selected_item):
    items = []
    for name, url in NAV_ITEMS:
        items.append({
            'name': name,
            'url': url,
            'active': True if selected_item == name else False
        })
    return items
