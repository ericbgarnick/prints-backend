import datetime
import os
from typing import List, Dict

from django.conf import settings

from catalog.models import Photo


# TODO: consolidate duplicated test helpers logic
def create_photo_data() -> List[Dict]:
    shot_date = datetime.date(year=1950, month=1, day=1)
    test_data = [
        {
            'image_id': 1,
            'title': 'one',
            'image_location': os.path.join('photos', '1.jpg'),
            'max_prints': 5,
            'shot_date': shot_date
        },
        {
            'image_id': 2,
            'title': 'two',
            'image_location': os.path.join('photos', '2.jpg'),
            'max_prints': 5,
            'shot_date': shot_date - datetime.timedelta(days=1)
        },
        {
            'image_id': 3,
            'title': 'three',
            'image_location': os.path.join('photos', '3.jpg'),
            'max_prints': 5,
            'shot_date': shot_date - datetime.timedelta(days=2)
        }
    ]
    photos = [Photo(**p_data) for p_data in test_data]
    Photo.objects.bulk_create(photos)
    return test_data
