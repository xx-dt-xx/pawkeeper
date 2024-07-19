from rest_framework import serializers


class VetNameMixin(serializers.ModelSerializer):
    vet_name = serializers.SerializerMethodField()

    def get_vet_name(self, obj):
        return obj.vet.name if obj.vet else None
