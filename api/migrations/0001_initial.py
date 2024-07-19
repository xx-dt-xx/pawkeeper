# Generated by Django 5.0.7 on 2024-07-17 23:04

import api.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergen', models.CharField(max_length=100)),
                ('reaction', models.TextField()),
                ('date_of_diagnosis', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Breeds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, validators=[api.validators.validate_alpha])),
            ],
        ),
        migrations.CreateModel(
            name='Illnesses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_of_diagnosis', models.DateField()),
                ('recovery_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PetGroomers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('NB', 'Non-Binary')], max_length=2)),
                ('email', models.CharField(max_length=250, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PetOwners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_type', models.CharField(choices=[('P', 'Primary'), ('S', 'Secondary')], default='P', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Pets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('sex', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=2)),
                ('birthdate', models.DateField()),
                ('color', models.CharField(max_length=100, validators=[api.validators.validate_alpha])),
            ],
        ),
        migrations.CreateModel(
            name='PetSalons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=250, null=True)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='PetTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[api.validators.validate_alpha])),
            ],
        ),
        migrations.CreateModel(
            name='Procedures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Surgeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Treatments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('lab_name', models.CharField(max_length=100)),
                ('lot', models.IntegerField()),
                ('expiration_date', models.DateField()),
                ('application_date', models.DateField()),
                ('next_due_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VetClinics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=250)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Vets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('NB', 'Non-Binary')], max_length=2)),
                ('email', models.CharField(max_length=250)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='VetVisits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('reason', models.TextField()),
                ('outcome', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WeighIns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='GroomingAppointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grooming_type', models.CharField(max_length=100)),
                ('notes', models.TextField(null=True)),
                ('date', models.DateTimeField()),
                ('pet_groomer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.petgroomers')),
            ],
        ),
    ]