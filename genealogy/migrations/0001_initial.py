# Generated by Django 5.0.7 on 2024-08-04 14:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('person_id', models.IntegerField(db_column='person_id', primary_key=True, serialize=False)),
                ('surname', models.CharField(db_column='surname', max_length=100)),
                ('maiden_name', models.CharField(blank=True, db_column='maiden_name', max_length=100, null=True)),
                ('name', models.CharField(db_column='name', max_length=100)),
                ('patronymic', models.CharField(blank=True, db_column='patronymic', max_length=100)),
                ('gender', models.CharField(db_column='gender', max_length=1)),
                ('date_of_birth', models.CharField(blank=True, db_column='date_of_birth', max_length=10, null=True)),
                ('date_of_death', models.CharField(blank=True, db_column='date_of_death', max_length=10, null=True)),
                ('person_father_id', models.IntegerField(blank=True, db_column='person_father_id', null=True)),
                ('person_mother_id', models.IntegerField(blank=True, db_column='person_mother_id', null=True)),
                ('note', models.CharField(blank=True, db_column='Note', max_length=255)),
                ('info', models.TextField(blank=True, db_column='info', null=True)),
                ('status', models.DecimalField(db_column='status', decimal_places=0, max_digits=1)),
                ('edit_date', models.DateTimeField(auto_now=True, db_column='edit_date')),
                ('father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fathers', to='genealogy.persons')),
                ('mother', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mothers', to='genealogy.persons')),
            ],
            options={
                'db_table': 'persons',
                'managed': True,
            },
        ),
    ]
