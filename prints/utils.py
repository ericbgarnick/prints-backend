from prints.models import PrintSize, PrintSizeInfo


def create_print_size_info():
    for size, base_price, ship_price in [(PrintSize.SMALL, 1000, 499),
                                         (PrintSize.MEDIUM, 1500, 599),
                                         (PrintSize.LARGE, 2000, 799)]:
        PrintSizeInfo.objects.get_or_create(size=size,
                                            base_price_cents=base_price,
                                            ship_price_cents=ship_price)
