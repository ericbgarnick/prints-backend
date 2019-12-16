import datetime
from enum import Enum
from typing import Union, List

from django.db.models import QuerySet, Count

from photos.models import Photo


class OrderBy(Enum):
    SHOT_DATE = "SHOT_DATE"
    POPULAR = "POPULAR"


# TODO: UT
def create_photos(num_photos: int = 100):
    """Create num_photos Photos in the DB for testing"""
    photos_to_create = []
    start_date = datetime.date(year=2000, month=1, day=1)
    base_num_prints = 10
    for i in range(num_photos):
        shot_date = start_date + datetime.timedelta(days=i)
        p = Photo(image_id=i, image_location='photos',
                  title=f'photo{i}', shot_date=shot_date,
                  max_prints=i % base_num_prints + base_num_prints)
        photos_to_create.append(p)
    Photo.objects.bulk_create(photos_to_create)


def ordered_photos(order_by: str) -> Union[QuerySet, List[Photo]]:
    base_photo_query = Photo.objects.all()

    if order_by.upper() == OrderBy.SHOT_DATE.value:
        photos = base_photo_query.order_by('-shot_date')
    elif order_by.upper() == OrderBy.POPULAR.value:
        photos = base_photo_query.annotate(print_count=Count('print'))\
            .order_by('-print_count')
    else:
        photos = base_photo_query

    return photos
