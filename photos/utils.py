import datetime

from photos.models import Photo


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
