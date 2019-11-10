from typing import Dict, List

from prints.models import PrintSize, PrintSizeInfo


def create_print_size_info_data() -> List[Dict]:
    test_data = [{'base_price_cents': 1000,
                  'ship_price_cents': 499,
                  'size': PrintSize.SMALL},
                 {'base_price_cents': 1500,
                  'ship_price_cents': 599,
                  'size': PrintSize.MEDIUM},
                 {'base_price_cents': 2000,
                  'ship_price_cents': 799,
                  'size': PrintSize.LARGE}]
    psi = [PrintSizeInfo(**psi_data) for psi_data in test_data]
    PrintSizeInfo.objects.bulk_create(psi)
    return test_data
