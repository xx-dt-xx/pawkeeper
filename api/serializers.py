# Handle data conversion and validation
from rest_framework import serializers
from .models import (
    PetTypes, Breeds, Pets, PetOwners, VetClinics, Vets, Allergies,
    WeighIns, Surgeries, Procedures, VetVisits, Vaccines, Illnesses,
    Treatments, PetSalons, PetGroomers, GroomingAppointments
)
from .mixins import VetNameMixin
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
    class Meta:
        model = Allergies
        fields = ['id', 'url', 'pet_id', 'allergen', 'reaction', 'date_of_diagnosis']


class WeighInsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WeighIns
        fields = ['id', 'url', 'pet_id', 'date', 'weight']


class SurgeriesSerializer(VetNameMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Surgeries
        fields = ['id', 'url', 'pet_id', 'date', 'name', 'description', 'vet_name']


class ProceduresSerializer(VetNameMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Procedures
        fields = ['id', 'url', 'pet_id', 'date', 'name', 'description', 'vet_name']


class VetVisitsSerializer(VetNameMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VetVisits
        fields = ['id', 'url', 'pet_id', 'date', 'reason', 'outcome', 'vet_name']


class VaccinesSerializer(VetNameMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vaccines
        fields = ['id', 'url', 'pet_id', 'name', 'lab_name', 'lot', 'expiration_date', 'application_date', 'next_due_date', 'vet_name']


class IllnessesSerializer(VetNameMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Illnesses
        fields = ['id', 'url', 'pet_id', 'name', 'description', 'date_of_diagnosis', 'recovery_date', 'vet_name']


class TreatmentsSerializer(VetNameMixin, serializers.HyperlinkedModelSerializer):
    illness_name = serializers.StringRelatedField(source='illness.name')

    class Meta:
        model = Treatments
        fields = ['id', 'url', 'name', 'illness_name', 'description', 'start_date', 'end_date', 'vet_name']


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
    pet_salon = PetSalonsSerializer()

    class Meta:
        model = PetGroomers
        fields = ['id', 'url', 'name', 'pet_salon']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not self.context.get('show_sensitive_info', False):
            data.pop('gender', None)
            data.pop('email', None)
            data.pop('phone', None)
        return data


class GroomingAppointmentsSerializer(serializers.HyperlinkedModelSerializer):
    pet_groomer = PetGroomersSerializer()

    class Meta:
        model = GroomingAppointments
        fields = ['id', 'url', 'pet_id', 'grooming_type', 'notes', 'date', 'pet_groomer', 'pet_salon']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        pet_groomer = instance.pet_groomer
        if pet_groomer and pet_groomer.pet_salon:
            representation['pet_salon'] = PetSalonsSerializer(pet_groomer.pet_salon).data
        return representation
