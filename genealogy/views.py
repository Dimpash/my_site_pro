from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from csv import DictReader
from os import path as os_path
from .models import Persons, Couples
from .forms import PersonsFilterForm, DescendantsForm, SelectPersonForm
from pprint import pprint


########################################
#  Render start page
########################################
def genealogy_menu(request):
    # context = {}
    # if request.user.is_authenticated:
    #     context['login_modal'] = 'fade'
    # else:
    #     context['login_modal'] = 'show'
    # return render(request, 'genealogy/genealogy_index.html')
    return render(request, 'genealogy/genealogy_index.html', {'func': 'menu'})


def login_view(request):
    # if request.user.is_authenticated:
    #     print('!!!!!!!!!!!!!!!!!!!!!')
    # else:
    #     print('@@@@@@@@@@@@@@@@@@@')
    return render(request, 'genealogy/login.html')


########################################
#  Login function
########################################
@csrf_exempt
def auth(request):
    user = None
    if request.method == 'POST':
        if ('username' in request.POST) and ('password' in request.POST):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            # return render(request, 'genealogy/genealogy_index.html')
            return redirect('menu')
    else:
        return HttpResponse('Wrong data')


########################################
#  Logout function
########################################
def logout_user(request):
    logout(request)
    return redirect('menu')


########################################
#  Function for full reload genealogy persons
########################################
@login_required
def genealogy_data_reload(request):
    # Delete (status = 0) old records
    couples = Couples.objects.all()
    for couple in couples:
        couple.delete()

    persons = Persons.objects.all()
    for person in persons:
        person.status = 0
        person.save()

    # Select new data
    with open("media/genealogy/Genealogy.csv", 'r') as f:
        dict_reader = DictReader(f, delimiter=';')
        list_of_dict = list(dict_reader)

    # Save new basic data
    for item in list_of_dict:
        person = Persons(
            person_id=int(item['person_id']),
            surname=item['surname'],
            maiden_name=item['maiden_name'],
            name=item['name'],
            patronymic=item['patronymic'],
            gender=item['gender'],
            date_of_birth=item['date_of_birth'],
            date_of_death=item['date_of_death'],
            note=item['note'],
            info=item['info'],
            status=1
        )

        person.save()

    # Set parents
    for item in list_of_dict:
        to_update = False

        person = Persons.objects.get(person_id=int(item['person_id']))

        if item['father_id'] > '':
            father = Persons.objects.get(person_id=int(item['father_id']))
            person.father = father
            to_update = True

        if item['mother_id'] > '':
            mother = Persons.objects.get(person_id=int(item['mother_id']))
            person.mother = mother
            to_update = True

        if to_update:
            person.save()

    # Input couples
    for i in range(1, 6):
        spouse_field = f'spouse{i}_id'
        for item in list_of_dict:
            if (item['gender'] == 'm') and (item[spouse_field] > ''):
                he_id = int(item['person_id'])
                she_id = int(item[spouse_field])
                fltr = Q(status__gt=0) & Q(
                    he__person_id=he_id) & Q(she__person_id=she_id)
                if not Couples.objects.filter(fltr).exists():
                    he = Persons.objects.get(person_id=he_id)
                    she = Persons.objects.get(person_id=she_id)
                    couple = Couples(
                        he=he,
                        she=she,
                        note=he.__str__() + ' - ' + she.__str__(),
                        status=1
                    )
                    couple.save()
    return HttpResponse('Data has been updated.')


########################################
# Класс отбора списка персоналий генеалогии
########################################
class PersonsListView(LoginRequiredMixin, ListView):
    template_name = 'genealogy/persons.html'
    context_object_name = 'persons_list'

    # paginate_by = 1000  # if pagination is desired

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.surname = ''
        self.name = ''
        self.patronymic = ''
        self.update_get_params = ''

    def get(self, request, *args, **kwargs):
        if 'surname' in self.request.GET:
            self.surname = self.request.GET['surname']

        if 'name' in self.request.GET:
            self.name = self.request.GET['name']

        if 'patronymic' in self.request.GET:
            self.patronymic = self.request.GET['patronymic']

        fltr = (Q(status__gt=0))  # Condition for Status
        if self.surname > '':
            fltr = fltr & (Q(surname=self.surname) | Q(
                maiden_name=self.surname))  # Condition for Surname
        if self.name > '':
            fltr = fltr & (Q(name=self.name))  # Condition for Name

        if self.patronymic > '':
            fltr = fltr & (Q(patronymic=self.patronymic))  # Condition for Patronymic

        self.queryset = Persons.objects.filter(fltr).order_by(
            'surname', 'name', 'patronymic').select_related('father', 'mother')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Словарь для Initial формы
        init = {}
        init['surname'] = self.surname
        init['name'] = self.name
        init['patronymic'] = self.patronymic

        portraits = {}
        for item in self.queryset:
            check_path = f'genealogy/static/genealogy/img/portrait/{item.person_id}.jpg'
            if os_path.exists(check_path):
                portrait_path = f'genealogy/img/portrait/{item.person_id}.jpg'
            elif item.gender == 'm':
                portrait_path = 'genealogy/img/portrait/male.jpg'
            else:
                portrait_path = 'genealogy/img/portrait/female.jpg'
            portraits[item.person_id] = portrait_path

        context['persons_filter_form'] = PersonsFilterForm(init)
        context['portraits'] = portraits
        context['init'] = init
        context['func'] = 'persons'

        return context

    def get_queryset(self):
        return self.queryset


########################################
# Класс отбора личной карточки
########################################
class PersonalCardDetailView(LoginRequiredMixin, DetailView):
    template_name = 'genealogy/personal_card.html'
    context_object_name = 'personal_card'
    model = Persons

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #  Select children
        fltr = Q(status__gt=0)  # Condition for Status
        if self.object.gender == 'm':
            # Condition for children by father
            fltr = fltr & Q(father__person_id=self.object.person_id)
        elif self.object.gender == 'f':
            # Condition for children by mother
            fltr = fltr & Q(mother__person_id=self.object.person_id)
        children = Persons.objects.filter(fltr).order_by(
            'surname', 'name', 'patronymic')

        # Select spouses
        fltr = Q(status__gt=0)  # Condition for Status
        if self.object.gender == 'm':
            # Condition for spouses by husband
            fltr = fltr & Q(he__person_id=self.object.person_id)
        elif self.object.gender == 'f':
            # Condition for spouses by wife
            fltr = fltr & Q(she__person_id=self.object.person_id)
        couples = Couples.objects.filter(fltr).order_by('couple_id')
        spouses = []
        for couple in couples:
            if self.object.gender == 'm':
                spouses.append(couple.she)
            elif self.object.gender == 'f':
                spouses.append(couple.he)

        # Select portrait photo
        check_path = f'genealogy/static/genealogy/img/portrait/{self.object.person_id}.jpg'
        if os_path.exists(check_path):
            portrait_path = f'genealogy/img/portrait/{self.object.person_id}.jpg'
        elif self.object.gender == 'm':
            portrait_path = 'genealogy/img/portrait/male.jpg'
        else:
            portrait_path = 'genealogy/img/portrait/female.jpg'

        context['children'] = children
        context['spouses'] = spouses
        context['portrait'] = portrait_path

        return context


# Get children tree as lists
# def get_children_tree_list(parent: Persons, children: list, lvl: int):
#     fltr = Q(status__gt=0) & (Q(father__person_id=parent.person_id)
#                               | Q(mother__person_id=parent.person_id))
#     children_queryset = Persons.objects.filter(fltr)

#     if children_queryset:
#         level = []

#         next_lvl = lvl + 1
#         for child in children_queryset:
#             level.append([next_lvl, child])
#             get_children_tree_list(parent=child, children=level, lvl=next_lvl)
#         children.append(level)

# def get_children_tree_list(parent: Persons, children: list, lvl: int, start: bool):
#     if start:
#         children_queryset = [parent]
#     else:
#         fltr = Q(status__gt=0) & (Q(father__person_id=parent.person_id)
#                                   | Q(mother__person_id=parent.person_id))
#         children_queryset = Persons.objects.filter(fltr)

#     if children_queryset:
#         # level = []

#         next_lvl = lvl + 1
#         for child in children_queryset:
#             children.append([next_lvl, child, child.__str__()])
#             get_children_tree_list(
#                 parent=child, children=children, lvl=next_lvl, start=False)
        # children.append(level)


# Get children tree as html code to implement
def get_descendants_tree_html(parent: Persons, tree_html: list, start: bool, br: str, show_spouses: int):
    if start:
        children_queryset = [parent]
    else:
        fltr = Q(status__gt=0) & (Q(father__person_id=parent.person_id)
                                  | Q(mother__person_id=parent.person_id))
        children_queryset = Persons.objects.filter(fltr)

    if children_queryset:
        tree_html.append('<ul>')
        for child in children_queryset:
            # print(child.__str__())
            check_path = f'genealogy/static/genealogy/img/portrait/{child.person_id}.jpg'
            if os_path.exists(check_path):
                portrait_img = f'<img src="/static/genealogy/img/portrait/{child.person_id}.jpg" height="50">'
                portrait_html = f'<div class="col-md-auto" style="padding: 0px 10px;" align="center">{portrait_img}</div>'
            else:
                portrait_html = ''
            if child.gender == 'f':
                gender_class = 'class="female"'
            else:
                gender_class = 'class="male"'
            # Формируем HTML для потомка
            name_html = f'<div class="col" style="padding: 0px 10px;">{child.__str__().replace(" ", br)}</div>'
            row_html = f'<div class="row justify-content-md-center">{portrait_html}{name_html}</div>'
            link_html = f'<a {gender_class} href="personal_card/{child.person_id}">{row_html}</a>'
            child_html = f'<li>{link_html}'
            # child_html = f'<li><a {gender_class} href="personal_card/{child.person_id}"><div class="row justify-content-md-center">{
            #     portrait_html}<div class="col" style="padding: 0px 10px;">{child.__str__().replace(' ', br)}</div></div></a>'

            # Отбираем супругов потомка
            if show_spouses == 1:
                fltr_s = Q(status__gt=0) & (
                    Q(he__person_id=child.person_id) | Q(she__person_id=child.person_id))
                couples_queryset = Couples.objects.filter(fltr_s)
                for couple in couples_queryset:
                    if couple.he.person_id == child.person_id:
                        spouse = couple.she
                    else:
                        spouse = couple.he
                    check_path = f'genealogy/static/genealogy/img/portrait/{spouse.person_id}.jpg'
                    if os_path.exists(check_path):
                        s_portrait_img = f'<img src="/static/genealogy/img/portrait/{spouse.person_id}.jpg" height="50">'
                        s_portrait_html = f'<div class="col-md-auto" style="padding: 0px 10px;" align="center">{s_portrait_img}</div>'
                    else:
                        s_portrait_html = ''
                    s_gender_class = 'class="spouse"'

                    name_html = f'<div class="col" style="padding: 0px 10px;">{spouse.__str__().replace(" ", br)}</div>'
                    row_html = f'<div class="row justify-content-md-center">{s_portrait_html}{name_html}</div>'
                    link_html = f'<a {s_gender_class} href="personal_card/{spouse.person_id}">{row_html}</a>'
                    child_html += link_html
                    # child_html += f'<a {s_gender_class} href="personal_card/{spouse.person_id}"><div class="row justify-content-md-center">{
                    #                     s_portrait_html}<div class="col" style="padding: 0px 10px;">{spouse.__str__().replace(' ', br)}</div></div></a>'
            tree_html.append(child_html)
            get_descendants_tree_html(
                parent=child,
                tree_html=tree_html,
                start=False,
                br=br,
                show_spouses=show_spouses
            )
            tree_html.append('</li>')
        tree_html.append('</ul>')


# Get ancestors tree as html code to implement
def get_ancestors_tree_html(person: Persons, tree_html: list, start: bool, br: str):
    if start:
        parents_queryset = [person]
    else:
        if person.father and person.mother:
            fltr = Q(status__gt=0) & (Q(person_id=person.father.person_id) | Q(
                person_id=person.mother.person_id))
        elif person.father:
            fltr = Q(status__gt=0) & Q(person_id=person.father.person_id)
        elif person.mother:
            fltr = Q(status__gt=0) & Q(person_id=person.mother.person_id)
        else:
            fltr = Q(status=-5)
        parents_queryset = Persons.objects.filter(fltr).order_by('-gender')

    # print(person.person_id, '=', person.surname, '=', person.name)

    if parents_queryset:
        tree_html.append('<ul>')
        for parent in parents_queryset:
            # print(parent.__str__())
            check_path = f'genealogy/static/genealogy/img/portrait/{parent.person_id}.jpg'
            if os_path.exists(check_path):
                portrait_img = f'<img src="/static/genealogy/img/portrait/{parent.person_id}.jpg" height="50">'
                portrait_html = f'<div class="col-md-auto" style="padding: 0px 10px;" align="center">{portrait_img}</div>'
            else:
                portrait_html = ''
            if parent.gender == 'f':
                gender_class = 'class="female"'
            else:
                gender_class = 'class="male"'
            name_html = f'<div class="col" style="padding: 0px 10px;">{parent.__str__().replace(" ", br)}</div>'
            row_html = f'<div class="row justify-content-md-center">{portrait_html}{name_html}</div>'
            link_html = f'<a {gender_class} href="personal_card/{parent.person_id}">{row_html}</a>'
            parent_html = f'<li>{link_html}'
            # parent_html = f'<li><a {gender_class} href="personal_card/{parent.person_id}"><div class="row justify-content-md-center">{portrait_html}<div class="col" style="padding: 0px 10px;">{parent.__str__().replace(' ', br)}</div></div></a>'
            tree_html.append(parent_html)
            get_ancestors_tree_html(
                person=parent,
                tree_html=tree_html,
                start=False,
                br=br
            )
            tree_html.append('</li>')
        tree_html.append('</ul>')


########################################
#  Function for descendants of the person
########################################
@login_required
def descendants(request):
    if 'view_type' in request.GET and request.GET['view_type'] == '1':
        view_type = 1
        br = ' '
        tree_css = 'genealogy/css/tree_h.css'
    else:
        view_type = 0
        br = '<br>'
        tree_css = 'genealogy/css/tree_v.css'

    if 'show_spouses' in request.GET:
        show_spouses = int(request.GET['show_spouses'])
    else:
        show_spouses = 0    

    children_tree_list = []
    tree_html_list = []

    if 'person' in request.GET:
        person_id = int(request.GET['person'])

        fltr = Q(status__gt=0) & Q(person_id=person_id)

        queryset = Persons.objects.filter(fltr)
        parent = queryset.first()
        # print('1. ', parent.surname)

        # get_children_tree_list(
        #     parent=parent,
        #     children=children_tree_list,
        #     lvl=0,
        #     start=True)

        get_descendants_tree_html(
            parent=parent,
            tree_html=tree_html_list,
            start=True,
            br=br,
            show_spouses=show_spouses)
        n = 0
        for child in children_tree_list:
            child.append(child[0] - n)
            n = child[0]
            # if child[0] > n:
            #     child.append('down')
            #     n = child[0]
            # elif child[0] < n:
            #     child.append('up')
            #     n = child[0]
            # else:
            #     child.append('=')

        # pprint(children_tree_list)

        tree_html = f'<div class="tree">'
        for item in tree_html_list:
            tree_html += item
        tree_html += '</div>'
        # pprint(tree_html)
        # Словарь для Initial формы
        init = {'person': parent,
                'view_type': view_type}
        person_id = parent.person_id
        view_type_id = view_type
        show_spouses_id = show_spouses
        # print(init)
    else:
        init = {}
        person_id = 0
        view_type_id = 0
        show_spouses_id = 1
        tree_html = ''

    return render(request,
                  'genealogy/descendants.html',
                  {'tree_html': tree_html,
                   'tree_css': tree_css,
                   'descendants_form': DescendantsForm(init),
                   'children': children_tree_list,
                   'person_id': person_id,
                   'view_type_id': view_type_id,
                   'show_spouses_id': show_spouses_id,
                   'func': 'descendants'
                   }
                  )


########################################
#  Function for ancestors of the person
########################################
@login_required
def ancestors(request):
    if 'view_type' in request.GET and request.GET['view_type'] == '1':
        view_type = 1
        br = ' '
        tree_css = 'genealogy/css/tree_h.css'
    else:
        view_type = 0
        br = '<br>'
        tree_css = 'genealogy/css/tree_v.css'

    parents_tree_list = []
    tree_html_list = []

    if 'person' in request.GET:
        person_id = int(request.GET['person'])

        fltr = Q(status__gt=0) & Q(person_id=person_id)

        queryset = Persons.objects.filter(fltr)
        person = queryset.first()

        get_ancestors_tree_html(
            person=person,
            tree_html=tree_html_list,
            start=True,
            br=br)

        tree_html = f'<div class="tree">'
        for item in tree_html_list:
            tree_html += item
        tree_html += '</div>'
        # Словарь для Initial формы
        init = {'person': person,
                'view_type': view_type}
        person_id = person.person_id
        view_type_id = view_type
    else:
        init = {}
        person_id = 0
        view_type_id = 0
        tree_html = ''

    return render(request,
                  'genealogy/ancestors.html',
                  {'tree_html': tree_html,
                   'tree_css': tree_css,
                   'select_person_form': SelectPersonForm(init),
                   #    'children': children_tree_list,
                   'person_id': person_id,
                   'view_type_id': view_type_id,
                   'func': 'ancestors'
                   }
                  )
