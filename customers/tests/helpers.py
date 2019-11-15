from typing import Dict

from geospatial.models import Address


def create_customer_data(address: Address) -> Dict:
    return {
        "first_name": "Test",
        "last_name": "McTest",
        "email": "test@test.com",
        "phone": "+13334445555",
        "address": address}
