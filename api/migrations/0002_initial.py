# Generated by Django 5.0.7 on 2024-07-17 23:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='petowners',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pets',
            name='breed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.breeds'),
        ),
        migrations.AddField(
            model_name='petowners',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pets'),
        ),
        migrations.AddField(
            model_name='illnesses',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='illnesses', to='api.pets'),
        ),
        migrations.AddField(
            model_name='groomingappointments',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grooming_appointments', to='api.pets'),
        ),
        migrations.AddField(
            model_name='allergies',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allergies', to='api.pets'),
        ),
        migrations.AddField(
            model_name='petgroomers',
            name='pet_salon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.petsalons'),
        ),
        migrations.AddField(
            model_name='groomingappointments',
            name='pet_salon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.petsalons'),
        ),
        migrations.AddField(
            model_name='pets',
            name='pet_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.pettypes'),
        ),
        migrations.AddField(
            model_name='breeds',
            name='pet_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pet_breeds', to='api.pettypes'),
        ),
        migrations.AddField(
            model_name='procedures',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='procedures', to='api.pets'),
        ),
        migrations.AddField(
            model_name='surgeries',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surgeries', to='api.pets'),
        ),
        migrations.AddField(
            model_name='treatments',
            name='illness',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='treatments', to='api.illnesses'),
        ),
        migrations.AddField(
            model_name='vaccines',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccines', to='api.pets'),
        ),
        migrations.AddField(
            model_name='vets',
            name='vet_clinic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vetclinics'),
        ),
        migrations.AddField(
            model_name='vaccines',
            name='vet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vets'),
        ),
        migrations.AddField(
            model_name='treatments',
            name='vet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vets'),
        ),
        migrations.AddField(
            model_name='surgeries',
            name='vet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vets'),
        ),
        migrations.AddField(
            model_name='procedures',
            name='vet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vets'),
        ),
        migrations.AddField(
            model_name='illnesses',
            name='vet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vets'),
        ),
        migrations.AddField(
            model_name='allergies',
            name='vet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vets'),
        ),
        migrations.AddField(
            model_name='vetvisits',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vet_visits', to='api.pets'),
        ),
        migrations.AddField(
            model_name='vetvisits',
            name='vet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vets'),
        ),
        migrations.AddField(
            model_name='weighins',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weigh_ins', to='api.pets'),
        ),
    ]
