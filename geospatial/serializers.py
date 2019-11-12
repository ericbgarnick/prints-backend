from rest_framework import serializers

from geospatial.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'unit', 'city', 'state', 'postal_code']
