from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from geospatial.models import Address
from geospatial.serializers import AddressSerializer
from orders.models import Payment, PaymentMethod, CreditNetwork
from utils.serializer_utils import (enum_from_str, check_numeric_string,
                                    check_str_length)


class PaymentSerializer(serializers.ModelSerializer):
    billing_address = AddressSerializer()
    method = serializers.ChoiceField(
        choices=[ps[1] for ps in PaymentMethod.choices()]
    )
    credit_network = serializers.ChoiceField(
        choices=[ps[1] for ps in CreditNetwork.choices()]
    )

    class Meta:
        model = Payment
        fields = ['method', 'credit_network', 'account_number',
                  'card_expiration', 'card_cvv', 'billing_first_name',
                  'billing_last_name', 'billing_address']

    def is_valid(self, raise_exception=False):
        method = self.initial_data.get('method')
        network = self.initial_data.get('credit_network')
        acct_num = self.initial_data.get('account_number')
        card_exp = self.initial_data.get('card_expiration')
        card_cvv = self.initial_data.get('card_cvv')
        billing_first_name = self.initial_data.get('billing_first_name')
        billing_last_name = self.initial_data.get('billing_last_name')
        billing_addr = self.initial_data.get('billing_address')

        # These instance vars must be created here
        self._errors = []
        self._validated_data = self.initial_data

        enum_from_str(method, PaymentMethod, self._errors)
        enum_from_str(network, CreditNetwork, self._errors)
        check_numeric_string(acct_num, Payment, 'account_number', self._errors)
        check_numeric_string(card_exp, Payment, 'card_expiration', self._errors)
        check_numeric_string(card_cvv, Payment, 'card_cvv', self._errors)
        check_str_length(billing_first_name, Payment, 'billing_first_name', self._errors)
        check_str_length(billing_last_name, Payment, 'billing_last_name', self._errors)
        addr_serializer = AddressSerializer(data=billing_addr)
        if not addr_serializer.is_valid():
            self._errors.append(f"Invalid address data {billing_addr}")

        if self._errors and raise_exception:
            raise ValidationError(self._errors)

        return not bool(self._errors)

    def create(self, validated_data):
        method = enum_from_str(validated_data.pop('method'), PaymentMethod)
        network = enum_from_str(validated_data.pop('credit_network'),
                                CreditNetwork)
        addr_data = validated_data.pop('billing_address')
        addr_serializer = AddressSerializer(data=addr_data)
        addr_serializer.is_valid()
        address, _ = Address.objects.get_or_create(**addr_serializer.data)
        return Payment.objects.create(method=method,
                                      credit_network=network,
                                      billing_address=address,
                                      **validated_data)
