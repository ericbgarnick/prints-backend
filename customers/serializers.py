from rest_framework import serializers

from customers.models import Customer
from geospatial.models import USAddress
from geospatial.serializers import USAddressSerializer


class CustomerSerializer(serializers.ModelSerializer):
    us_address = USAddressSerializer()

    class Meta:
        model = Customer
        fields = ['full_name', 'email', 'us_phone', 'us_address']

    def create(self, validated_data):
        address_data = validated_data.pop('us_address')
        address, _ = USAddress.objects.get_or_create(**address_data)
        return Customer.objects.create(us_address=address, **validated_data)
