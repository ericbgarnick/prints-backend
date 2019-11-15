from rest_framework import serializers

from customers.models import Customer
from geospatial.models import Address
from geospatial.serializers import AddressSerializer


class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address, _ = Address.objects.get_or_create(**address_data)
        return Customer.objects.create(address=address, **validated_data)
