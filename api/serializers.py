# Handle data conversion and validation
from rest_framework import serializers
from .models import (
    PetTypes, Breeds, Pets, PetOwners, VetClinics, Vets, Allergies,
    WeighIns, Surgeries, Procedures, VetVisits, Vaccines, Illnesses,
    Treatments, PetSalons, PetGroomers, GroomingAppointments
)
from .validators import validate_alpha


class PetTypesSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(validators=[validate_alpha])

    class Meta:
        model = PetTypes
        fields = ['id', 'url', 'name']

    def validate(self, data):
        # Check if a breed with the same name and pet type already exists
        if PetTypes.objects.filter(name__iexact=data['name']).exists():
            raise serializers.ValidationError("A pet type with this name already exists.")
        return data

    # Get pet type if it exists already or create a new pet type if it doesn't exist.
    def get_or_create(self, validated_data):
        name = validated_data.get('name')
        pet_type, created = PetTypes.objects.get_or_create(name=name)
        return pet_type


class BreedsSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(validators=[validate_alpha])
    pet_type = serializers.SerializerMethodField()
    pet_type_id = serializers.PrimaryKeyRelatedField(queryset=PetTypes.objects.all(), write_only=True, source='pet_type')

    class Meta:
        model = Breeds
        fields = ['id', 'url', 'name', 'pet_type', 'pet_type_id']

    def get_pet_type(self, instance):
        return {'id': instance.pet_type.id, 'name': instance.pet_type.name} if instance.pet_type else None

    def validate(self, data):
        # Check if a breed with the same name and pet type already exists
        if Breeds.objects.filter(name__iexact=data['name'], pet_type=data['pet_type']).exists():
            raise serializers.ValidationError("A breed with this name and pet type already exists.")
        return data

    def create(self, validated_data):
        # Extract pet_type from validated data.
        pet_type = validated_data.pop('pet_type')
        # Create a new breed instance with the rest of the validated data.
        breed = Breeds.objects.create(pet_type=pet_type, **validated_data)
        return breed

    def update(self, instance, validated_data):
        pet_type = validated_data.pop('pet_type')
        instance.name = validated_data.get('name', instance.name)
        instance.pet_type = pet_type
        instance.save()
        return instance


class PetsSerializer(serializers.HyperlinkedModelSerializer):
    pet_type = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    pet_type_id = serializers.PrimaryKeyRelatedField(queryset=PetTypes.objects.all(), write_only=True, source='pet_type')
    breed_id = serializers.PrimaryKeyRelatedField(queryset=Breeds.objects.all(), write_only=True, source='breed')
    color = serializers.CharField(validators=[validate_alpha])

    class Meta:
        model = Pets
        fields = ['id', 'url', 'name', 'sex', 'birthdate', 'color', 'pet_type', 'pet_type_id', 'breed', 'breed_id']

    def get_pet_type(self, instance):
        return {'id': instance.pet_type.id, 'name': instance.pet_type.name} if instance.pet_type else None

    def get_breed(self, instance):
        return {'id': instance.breed.id, 'name': instance.breed.name} if instance.breed else None

    def create(self, validated_data):
        # Extract pet_type and breed from validated data.
        pet_type = validated_data.pop('pet_type')
        breed = validated_data.pop('breed')

        # Create a new pet instance with the rest of the validated data.
        pet = Pets.objects.create(pet_type=pet_type, breed=breed, **validated_data)
        return pet

    def update(self, instance, validated_data):
        pet_type = validated_data.pop('pet_type')
        breed = validated_data.pop('breed')
        instance.name = validated_data.get('name', instance.name)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.color = validated_data.get('color', instance.color)
        instance.pet_type = pet_type
        instance.breed = breed
        instance.save()
        return instance


# Finish implementation after custom user implementation is done.
class PetOwnersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PetOwners
        fields = ['id', 'url', 'user_id', 'pet_id', 'owner_type']


class VetClinicsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VetClinics
        fields = ['id', 'url', 'name', 'address', 'email', 'phone']

    def validate(self, data):
        # Check if a vet clinic with the same fields already exists
        if VetClinics.objects.filter(name__iexact=data['name'], address__iexact=data['address']).exists():
            raise serializers.ValidationError("A vet clinic with the same name and address already exists.")
        return data


class VetsSerializer(serializers.HyperlinkedModelSerializer):
    vet_clinic = serializers.SerializerMethodField()
    vet_clinic_id = serializers.PrimaryKeyRelatedField(queryset=VetClinics.objects.all(), write_only=True, source='vet_clinic')

    class Meta:
        model = Vets
        fields = ['id', 'url', 'name', 'gender', 'email', 'phone', 'vet_clinic', 'vet_clinic_id']

    def validate(self, data):
        # Check if a vet with the same name and vet_clinic already exists
        if Vets.objects.filter(name__iexact=data['name'], vet_clinic__exact=data['vet_clinic']).exists():
            raise serializers.ValidationError("A vet with the same name and vet clinic already exists.")
        return data

    def get_vet_clinic(self, instance):
        return {'id': instance.vet_clinic.id, 'name': instance.vet_clinic.name, 'address': instance.vet_clinic.address} if instance.vet_clinic else None

    def create(self, validated_data):
        # Extract vet_clinic from validated data.
        vet_clinic = validated_data.pop('vet_clinic')

        # Create a new vet instance with the rest of the validated data.
        vet = Vets.objects.create(vet_clinic=vet_clinic, **validated_data)
        return vet

    def update(self, instance, validated_data):
        vet_clinic = validated_data.pop('vet_clinic')
        instance.name = validated_data.get('name')
        instance.gender = validated_data.get('gender')
        instance.email = validated_data.get('email')
        instance.phone = validated_data('phone')
        instance.vet_clinic = vet_clinic
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not self.context.get('show_sensitive_info', False):
            data.pop('gender', None)
            data.pop('email', None)
            data.pop('phone', None)
        return data


class AllergiesSerializer(serializers.HyperlinkedModelSerializer):
    pet = serializers.SerializerMethodField()

    class Meta:
        model = Allergies
        fields = ['id', 'url', 'pet', 'allergen', 'reaction', 'date_of_diagnosis']

    def validate(self, data):
        # Check if an allergy with the same pet, allergen and date_of_diagnosis already exists
        if Allergies.objects.filter(pet=data['pet'], allergen__iexact=data['allergen'], date_of_diagnosis__exact=data['date']).exists():
            raise serializers.ValidationError("Allergy has been previously recorded for the same date and pet.")
        return data

    def create(self, validated_data):
        # Extract pet from validated data.
        pet = validated_data.pop('pet')
        # Create a new allergy instance with the rest of the validated data.
        allergy = Allergies.objects.create(pet=pet, **validated_data)
        return allergy

    def update(self, instance, validated_data):
        pet = validated_data.pop('pet')
        instance.allergen = validated_data.get('allergen', instance.allergen)
        instance.reaction = validated_data.get('reaction', instance.reaction)
        instance.date_of_diagnosis = validated_data.get('date_of_diagnosis', instance.date_of_diagnosis)
        instance.pet = pet
        instance.save()
        return instance


class WeighInsSerializer(serializers.HyperlinkedModelSerializer):
    pet = serializers.SerializerMethodField()

    class Meta:
        model = WeighIns
        fields = ['id', 'url', 'pet', 'date', 'weight']

    def validate(self, data):
        # Check if a weigh_in with the same weight, pet and date already exists
        if WeighIns.objects.filter(pet=data['pet'], date__exact=data['date'], weight__exact=data['weight']).exists():
            raise serializers.ValidationError("Weight has been previously recorded for the same date and pet.")
        return data

    def create(self, validated_data):
        # Extract pet from validated data.
        pet = validated_data.pop('pet')
        # Create a new weigh_in instance with the rest of the validated data.
        weigh_in = WeighIns.objects.create(pet=pet, **validated_data)
        return weigh_in

    def update(self, instance, validated_data):
        pet = validated_data.pop('pet')
        instance.date = validated_data.get('date', instance.date)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.pet = pet
        instance.save()
        return instance


class SurgeriesSerializer(serializers.HyperlinkedModelSerializer):
    pet = serializers.SerializerMethodField()
    vet = serializers.SerializerMethodField()

    class Meta:
        model = Surgeries
        fields = ['id', 'url', 'pet', 'date', 'name', 'description', 'vet']

    def validate(self, data):
        # Check if a surgery with the same name, pet and date already exists
        if Surgeries.objects.filter(name__iexact=data['name'], pet=data['pet'], date__exact=data['date']).exists():
            raise serializers.ValidationError("A surgery with this name, pet and date already exists.")
        return data

    def create(self, validated_data):
        # Extract pet and vet from validated data.
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        # Create a new surgery instance with the rest of the validated data.
        surgery = Surgeries.objects.create(pet=pet, vet=vet, **validated_data)
        return surgery

    def update(self, instance, validated_data):
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        instance.date = validated_data.get('date', instance.date)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.pet = pet
        instance.vet = vet
        instance.save()
        return instance


class ProceduresSerializer(serializers.HyperlinkedModelSerializer):
    pet = serializers.SerializerMethodField()
    vet = serializers.SerializerMethodField()

    class Meta:
        model = Procedures
        fields = ['id', 'url', 'pet', 'date', 'name', 'description', 'vet']

    def validate(self, data):
        # Check if a procedure with the same name, pet and date already exists
        if Procedures.objects.filter(name__iexact=data['name'], pet=data['pet'], date__exact=data['date']).exists():
            raise serializers.ValidationError("A procedure with this name, pet and date already exists.")
        return data

    def create(self, validated_data):
        # Extract pet and vet from validated data.
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        # Create a new procedure instance with the rest of the validated data.
        procedure = Procedures.objects.create(pet=pet, vet=vet, **validated_data)
        return procedure

    def update(self, instance, validated_data):
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        instance.date = validated_data.get('date', instance.date)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.pet = pet
        instance.vet = vet
        instance.save()
        return instance


class VetVisitsSerializer(serializers.HyperlinkedModelSerializer):
    pet = serializers.SerializerMethodField()
    vet = serializers.SerializerMethodField()

    class Meta:
        model = VetVisits
        fields = ['id', 'url', 'pet', 'date', 'reason', 'outcome', 'vet']

    def validate(self, data):
        # Check if a vet visit with the same vet, pet and date already exists
        if VetVisits.objects.filter(pet=data['pet'], date__exact=data['date'], vet=data['vet']).exists():
            raise serializers.ValidationError("A vet visit with this pet, vet and date already exists.")
        return data

    def create(self, validated_data):
        # Extract pet and vet from validated data.
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        # Create a new vet_visit instance with the rest of the validated data.
        vet_visit = VetVisits.objects.create(pet=pet, vet=vet, **validated_data)
        return vet_visit

    def update(self, instance, validated_data):
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        instance.date = validated_data.get('date', instance.date)
        instance.reason = validated_data.get('reason', instance.reason)
        instance.outcome = validated_data.get('outcome', instance.outcome)
        instance.pet = pet
        instance.vet = vet
        instance.save()
        return instance


class VaccinesSerializer(serializers.HyperlinkedModelSerializer):
    pet = serializers.SerializerMethodField()
    vet = serializers.SerializerMethodField()

    class Meta:
        model = Vaccines
        fields = ['id', 'url', 'pet', 'name', 'lab_name', 'lot', 'expiration_date', 'application_date', 'next_due_date', 'vet']

    def validate(self, data):
        # Check if a vaccine with the same lot already exists
        if Vaccines.objects.filter(lot__exact=data['lot']).exists():
            raise serializers.ValidationError("A vaccine with this lot is already registered.")
        return data

    def create(self, validated_data):
        # Extract pet and vet from validated data.
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        # Create a new vaccine instance with the rest of the validated data.
        vaccine = Vaccines.objects.create(pet=pet, vet=vet, **validated_data)
        return vaccine

    def update(self, instance, validated_data):
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        instance.name = validated_data.get('name', instance.name)
        instance.lab_name = validated_data.get('lab_name', instance.lab_name)
        instance.lot = validated_data.get('lot', instance.lot)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.application_date = validated_data.get('application_date', instance.application_date)
        instance.next_due_date = validated_data.get('next_due_date', instance.next_due_date)
        instance.pet = pet
        instance.vet = vet
        instance.save()
        return instance


class IllnessesSerializer(serializers.HyperlinkedModelSerializer):
    pet = serializers.SerializerMethodField()
    vet = serializers.SerializerMethodField()

    class Meta:
        model = Illnesses
        fields = ['id', 'url', 'pet', 'name', 'description', 'date_of_diagnosis', 'recovery_date', 'vet']

    def validate(self, data):
        # Check if an illness with the same pet, name and date_of_diagnosis already exists
        if Illnesses.objects.filter(pet=data['pet'], name__iexact=data['name'], date_of_diagnosis__exact=data['date_of_diagnosis']).exists():
            raise serializers.ValidationError("An illness with this pet, name and date_of_diagnosis is already registered.")
        return data

    def create(self, validated_data):
        # Extract pet and vet from validated data.
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        # Create a new illness instance with the rest of the validated data.
        illness = Illnesses.objects.create(pet=pet, vet=vet, **validated_data)
        return illness

    def update(self, instance, validated_data):
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.date_of_diagnosis = validated_data.get('date_of_diagnosis', instance.date_of_diagnosis)
        instance.recovery_date = validated_data.get('recovery_date', instance.recovery_date)
        instance.pet = pet
        instance.vet = vet
        instance.save()
        return instance


class TreatmentsSerializer(serializers.HyperlinkedModelSerializer):
    pet = serializers.SerializerMethodField()
    vet = serializers.SerializerMethodField()
    illness = serializers.SerializerMethodField()
    illness_id = serializers.PrimaryKeyRelatedField(queryset=Illnesses.objects.all(), write_only=True, source='illness')

    class Meta:
        model = Treatments
        fields = ['id', 'url', 'pet', 'name', 'description', 'illness', 'illness_id', 'start_date', 'end_date', 'vet']

    def validate(self, data):
        # Check if a treatment with the same illness, name and start_date already exists
        if Treatments.objects.filter(illness=data['illness'], name__iexact=data['name'], start_date__exact=data['start_date']).exists():
            raise serializers.ValidationError("A treatment for this illness, name and start_date is already registered.")
        return data

    def get_illness(self, instance):
        return {'id': instance.illness.id, 'name': instance.illness.name} if instance.illness else None

    def create(self, validated_data):
        # Extract pet, vet and illness from validated data.
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        illness = validated_data.pop('illness')

        # Create a new treatment instance with the rest of the validated data.
        treatment = Treatments.objects.create(pet=pet, vet=vet, illness=illness, **validated_data)
        return treatment

    def update(self, instance, validated_data):
        pet = validated_data.pop('pet')
        vet = validated_data.pop('vet')
        illness = validated_data.pop('illness')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.pet = pet
        instance.vet = vet
        instance.illness = illness
        instance.save()
        return instance


class PetSalonsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PetSalons
        fields = ['id', 'url', 'name', 'address', 'email', 'phone']

    def validate(self, data):
        # Check if a pet salon with the same fields already exists
        if PetSalons.objects.filter(name__iexact=data['name'], address__iexact=data['address']).exists():
            raise serializers.ValidationError("A pet salon with the same name and address already exists.")
        return data


class PetGroomersSerializer(serializers.HyperlinkedModelSerializer):
    pet_salon = serializers.SerializerMethodField()
    pet_salon_id = serializers.PrimaryKeyRelatedField(queryset=PetSalons.objects.all(), write_only=True, source='pet_salon')

    class Meta:
        model = Vets
        fields = ['id', 'url', 'name', 'gender', 'email', 'phone', 'pet_salon', 'pet_salon_id']

    def validate(self, data):
        # Check if a pet groomer with the same name and pet_salon already exists
        if PetGroomers.objects.filter(name__iexact=data['name'], pet_salon__exact=data['pet_salon']).exists():
            raise serializers.ValidationError("A pet groomer with the same name and pet salon already exists.")
        return data

    def get_vet_clinic(self, instance):
        return {'id': instance.pet_salon.id, 'name': instance.pet_salon.name, 'address': instance.pet_salon.address} if instance.pet_salon else None

    def create(self, validated_data):
        # Extract pet_salon from validated data.
        pet_salon = validated_data.pop('pet_salon')

        # Create a new pet groomer instance with the rest of the validated data.
        groomer = PetGroomers.objects.create(pet_salon=pet_salon, **validated_data)
        return groomer

    def update(self, instance, validated_data):
        pet_salon = validated_data.pop('pet_salon')
        instance.name = validated_data.get('name')
        instance.gender = validated_data.get('gender')
        instance.email = validated_data.get('email')
        instance.phone = validated_data('phone')
        instance.pet_salon = pet_salon
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not self.context.get('show_sensitive_info', False):
            data.pop('gender', None)
            data.pop('email', None)
            data.pop('phone', None)
        return data


class GroomingAppointmentsSerializer(serializers.HyperlinkedModelSerializer):
    pet = serializers.SerializerMethodField()
    pet_groomer = serializers.SerializerMethodField()

    class Meta:
        model = GroomingAppointments
        fields = ['id', 'url', 'pet', 'grooming_type', 'notes', 'date', 'pet_groomer', 'pet_salon']

    def validate(self, data):
        # Check if a grooming_appointment with the same pet, pet_groomer and date already exists
        if GroomingAppointments.objects.filter(pet=data['pet'], date__exact=data['date'], pet_groomer=data['pet_groomer']).exists():
            raise serializers.ValidationError("A vet visit with this pet, pet_groomer and date already exists.")
        return data

    def create(self, validated_data):
        # Extract pet and pet_groomer from validated data.
        pet = validated_data.pop('pet')
        pet_groomer = validated_data.pop('pet_groomer')
        # Create a new grooming_appointment instance with the rest of the validated data.
        grooming_appointment = VetVisits.objects.create(pet=pet, pet_groomer=pet_groomer, **validated_data)
        return grooming_appointment

    def update(self, instance, validated_data):
        pet = validated_data.pop('pet')
        pet_groomer = validated_data.pop('pet_groomer')
        instance.grooming_type = validated_data.get('grooming_type', instance.grooming_type)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.date = validated_data.get('date', instance.date)
        instance.pet = pet
        instance.pet_groomer = pet_groomer
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        pet_groomer = instance.pet_groomer
        if pet_groomer and pet_groomer.pet_salon:
            representation['pet_salon'] = PetSalonsSerializer(pet_groomer.pet_salon).data
        return representation
