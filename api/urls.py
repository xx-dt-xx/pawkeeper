from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from . import views
import re


def camel_to_snake(name):
    # Convert CamelCase to snake_case.
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


router = routers.DefaultRouter()

# Dynamically register viewsets with the router
viewset_classes = {}
for model, serializer in views.viewsets_info:
    viewset_class = views.GenericViewSet.as_viewset(model, serializer)
    viewset_classes[model.__name__] = viewset_class
    router.register(camel_to_snake(model.__name__), viewset_class)


# Create a nested router for pets
pets_router = nested_routers.NestedDefaultRouter(router, r'pets', lookup='pet')

# Map related models to Pets
pet_related_models = [
    'Allergies', 'WeighIns', 'Surgeries', 'Procedures', 'VetVisits', 'Vaccines', 'Illnesses', 'GroomingAppointments'
]

for pet_related_model in pet_related_models:
    nested_viewset_class = viewset_classes[pet_related_model]
    pets_router.register(camel_to_snake(pet_related_model), nested_viewset_class, basename=f'pet_{camel_to_snake(pet_related_model)}')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(pets_router.urls)),
]
