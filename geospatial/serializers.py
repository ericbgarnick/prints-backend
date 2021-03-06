from rest_framework import serializers

from geospatial.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['line1', 'line2', 'city', 'state', 'postal_code', 'country']

    def create(self, validated_data):
        # Don't create duplicates
        return Address.objects.get_or_create(**validated_data)[0]
