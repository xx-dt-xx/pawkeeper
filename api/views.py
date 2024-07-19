from rest_framework import viewsets
from .models import (
    PetTypes, Breeds, Pets, PetOwners, VetClinics, Vets, Allergies,
    WeighIns, Surgeries, Procedures, VetVisits, Vaccines, Illnesses,
    Treatments, PetSalons, PetGroomers, GroomingAppointments
)
from .serializers import (
    PetTypesSerializer, BreedsSerializer, PetsSerializer, PetOwnersSerializer,
    VetClinicsSerializer, VetsSerializer, AllergiesSerializer, WeighInsSerializer,
    SurgeriesSerializer, ProceduresSerializer, VetVisitsSerializer, VaccinesSerializer,
    IllnessesSerializer, TreatmentsSerializer, PetSalonsSerializer, PetGroomersSerializer,
    GroomingAppointmentsSerializer
)


class GenericViewSet(viewsets.ModelViewSet):
    @classmethod
    def as_viewset(cls, model, serializer):
        return type(
            f"{model.__name__}ViewSet",
            (cls,),
            {
                "queryset": model.objects.all(),
                "serializer_class": serializer,
            }
        )


viewsets_info = [
    (PetTypes, PetTypesSerializer),
    (Breeds, BreedsSerializer),
    (Pets, PetsSerializer),
    (PetOwners, PetOwnersSerializer),
    (VetClinics, VetClinicsSerializer),
    (Vets, VetsSerializer),
    (Allergies, AllergiesSerializer),
    (WeighIns, WeighInsSerializer),
    (Surgeries, SurgeriesSerializer),
    (Procedures, ProceduresSerializer),
    (VetVisits, VetVisitsSerializer),
    (Vaccines, VaccinesSerializer),
    (Illnesses, IllnessesSerializer),
    (Treatments, TreatmentsSerializer),
    (PetSalons, PetSalonsSerializer),
    (PetGroomers, PetGroomersSerializer),
    (GroomingAppointments, GroomingAppointmentsSerializer),
]

# Dynamically create viewsets
globals().update({
    f"{model.__name__}ViewSet": GenericViewSet.as_viewset(model, serializer)
    for model, serializer in viewsets_info
})
