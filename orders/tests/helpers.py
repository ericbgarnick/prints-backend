from typing import Dict

from geospatial.models import Address


def create_payment_data(address: Address) -> Dict:
    return {'method': "Credit",
            'credit_network': 'Visa',
            'account_number': '0123456789012345',
            'card_expiration': '012020',
            'card_cvv': '1234',
            'billing_first_name': 'Account',
            'billing_last_name': 'Holder',
            'billing_address': address}
