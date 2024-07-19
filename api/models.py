from django.db import models
from authentication.models import CustomUser
from .validators import validate_alpha

GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('NB', 'Non-Binary'),
    )


class PetTypes(models.Model):
    name = models.CharField(max_length=100, validators=[validate_alpha])

    def __str__(self):
        return self.name


class Breeds(models.Model):
    name = models.CharField(max_length=200, validators=[validate_alpha])
    pet_type = models.ForeignKey(PetTypes, related_name='pet_breeds', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Pets(models.Model):
    SEX_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )

    name = models.CharField(max_length=200)
    sex = models.CharField(max_length=2, choices=SEX_CHOICES)
    birthdate = models.DateField()
    color = models.CharField(max_length=100, validators=[validate_alpha])
    pet_type = models.ForeignKey(PetTypes, on_delete=models.SET_NULL, null=True)
    breed = models.ForeignKey(Breeds, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"PID {self.id}"


class PetOwners(models.Model):
    OWNER_CHOICES = (
        ('P', 'Primary'),
        ('S', 'Secondary'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pets, on_delete=models.CASCADE)
    owner_type = models.CharField(max_length=2, choices=OWNER_CHOICES, default='P')


class VetClinics(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Vets(models.Model):
    name = models.CharField(max_length=250)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=15)
    vet_clinic = models.ForeignKey(VetClinics, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Allergies(models.Model):
    pet = models.ForeignKey(Pets, related_name='allergies', on_delete=models.CASCADE)
    allergen = models.CharField(max_length=100)
    reaction = models.TextField()
    date_of_diagnosis = models.DateField()
    vet = models.ForeignKey(Vets, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.allergen


class WeighIns(models.Model):
    pet = models.ForeignKey(Pets, related_name='weigh_ins', on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return f"{self.id}"


class Surgeries(models.Model):
    pet = models.ForeignKey(Pets, related_name='surgeries', on_delete=models.CASCADE)
    date = models.DateField()
    name = models.CharField(max_length=200)
    description = models.TextField()
    vet = models.ForeignKey(Vets, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id}"


class Procedures(models.Model):
    pet = models.ForeignKey(Pets, related_name='procedures', on_delete=models.CASCADE)
    date = models.DateField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    vet = models.ForeignKey(Vets, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id}"


class VetVisits(models.Model):
    pet = models.ForeignKey(Pets, related_name='vet_visits', on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    outcome = models.TextField()
    vet = models.ForeignKey(Vets, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id}"


class Vaccines(models.Model):
    pet = models.ForeignKey(Pets, related_name='vaccines', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lab_name = models.CharField(max_length=100)
    lot = models.IntegerField()
    expiration_date = models.DateField()
    application_date = models.DateField()
    next_due_date = models.DateField(null=True)
    vet = models.ForeignKey(Vets, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id}"


class Illnesses(models.Model):
    pet = models.ForeignKey(Pets, related_name='illnesses', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_of_diagnosis = models.DateField()
    recovery_date = models.DateField(null=True)
    vet = models.ForeignKey(Vets, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id}"


class Treatments(models.Model):
    illness = models.ForeignKey(Illnesses, related_name='treatments', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    vet = models.ForeignKey(Vets, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id}"


class PetSalons(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class PetGroomers(models.Model):
    name = models.CharField(max_length=250)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    email = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=15, null=True)
    pet_salon = models.ForeignKey(PetSalons, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class GroomingAppointments(models.Model):
    pet = models.ForeignKey(Pets, related_name='grooming_appointments', on_delete=models.CASCADE)
    grooming_type = models.CharField(max_length=100)
    notes = models.TextField(null=True)
    date = models.DateTimeField()
    pet_groomer = models.ForeignKey(PetGroomers, on_delete=models.SET_NULL, null=True)
    pet_salon = models.ForeignKey(PetSalons, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.id}"
