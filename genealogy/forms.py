from django import forms
from .models import *

# Класс для фильтра для просмотра персоналий генеалогии


class PersonsFilterForm(forms.Form):
    # surname = models.CharField(db_column='surname', max_length=100, blank=False, null=False)
    # maiden_name = models.CharField(db_column='maiden_name', max_length=100, blank=True, null=True)
    # name = models.CharField(db_column='name', max_length=100, blank=False, null=False)
    # patronymic = models.CharField(db_column='patronymic', max_length=100, blank=True, null=False)
    # gender = models.CharField(db_column='gender', max_length=1, blank=False, null=False)
    # date_of_birth = models.CharField(db_column='date_of_birth', max_length=10, blank=True, null=True)
    # date_of_death = models.CharField(db_column='date_of_death', max_length=10, blank=True, null=True)
    # # person_father_id = models.IntegerField(db_column='person_father_id', blank=True, null=True)
    # father = models.ForeignKey("self", related_name="fathers", on_delete=models.CASCADE, null=True, blank=True)
    # # person_mother_id = models.IntegerField(db_column='person_mother_id', blank=True, null=True)
    # mother = models.ForeignKey("self", related_name="mothers", on_delete=models.CASCADE, null=True, blank=True)

    surname = forms.CharField(max_length=100, required=False, label='Фамилия')
    name = forms.CharField(max_length=100, required=False, label='Имя')
    patronymic = forms.CharField(
        max_length=100, required=False, label='Отчество')
    # res = forms.ModelChoiceField(label='Привязка к РЭС', empty_label='< ВСЕ >', required=False,
    #                              queryset=SprRes.objects.filter(kpk__lte='3').order_by('resname'))
    # uch = forms.ModelChoiceField(label='Участок', empty_label='< ВСЕ >', required=False,
    #                              queryset=SprUch.objects.filter(uch_id__lte=23).order_by('uchname'))
    # show_deleted = forms.ChoiceField(choices=[(0, 'Нет'), (1, 'Да')], required=False, label='Показывать удаленные')

# Класс для фильтра для выбора персоналии генеалогии


class DescendantsForm(forms.Form):
    person = forms.ModelChoiceField( required=False,
                                     queryset=Persons.objects.filter(status__gt=0).order_by('surname', 'name', 'patronymic'))
    view_type = forms.ChoiceField(choices=[(0, 'Вертикальное древо'), (1, 'Горизонтальное древо ')], required=False)
    show_spouses = forms.ChoiceField(choices=[(0, 'Скрыть супругов'), (1, 'Показать супругов')], required=False)


class SelectPersonForm(forms.Form):
    person = forms.ModelChoiceField( required=False,
                                     queryset=Persons.objects.filter(status__gt=0).order_by('surname', 'name', 'patronymic'))
    view_type = forms.ChoiceField(choices=[(0, 'Вертикальное древо'), (1, 'Горизонтальное древо ')], required=False)