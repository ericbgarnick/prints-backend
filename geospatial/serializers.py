from rest_framework import serializers

from geospatial.models import USAddress


class USAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = USAddress
        fields = ['street', 'unit', 'city', 'state', 'postal_code']
