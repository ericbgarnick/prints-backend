import datetime

from django.test import TestCase

from photos.models import Photo
from prints.models import PrintSizeInfo, Print, PrintSize
from prints.serializers import PrintSizeInfoSerializer, PrintSerializer
from prints.tests.helpers import create_print_size_info_data


class TestPrintsSerializers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test data
        cls.test_data = create_print_size_info_data()

    @classmethod
    def tearDownClass(cls):
        Photo.objects.all().delete()
        Print.objects.all().delete()
        PrintSizeInfo.objects.all().delete()
        super().tearDownClass()

    def test_serialize_print_size_info(self):
        """Assert model instances are serialized as expected"""
        # Get serialized data
        all_psi = PrintSizeInfo.objects.all().order_by('base_price_cents')
        serialized_data = PrintSizeInfoSerializer(all_psi, many=True).data

        # Compare with test data
        self.assertEqual(len(serialized_data), len(self.test_data))
        for i, ser_d in enumerate(serialized_data):
            test_d = self.test_data[i]
            # Serializer converts Enum to str
            test_d['size'] = str(test_d['size'])
            self.assertDictEqual(dict(ser_d), test_d)

    def test_create_print_valid_data(self):
        """Assert the PrintSerializer successfully
        creates a new instance from valid data"""
        size = 'MEDIUM'
        size_info = PrintSizeInfo.objects.get(size=PrintSize[size])
        shot_date = datetime.date(year=2000, month=1, day=1)
        photo = Photo.objects.create(image_id=1, image_location='photos',
                                     title='photo1', shot_date=shot_date,
                                     max_prints=10)
        print_data = {'size_info__size': size, 'photo__image_id': photo.image_id}
        serializer = PrintSerializer(data=print_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        created_print = Print.objects.filter(size_info=size_info, photo=photo,
                                             print_number=1)
        self.assertTrue(created_print.exists())

    def test_create_print_invalid_data(self):
        """Assert the PrintSerializer does not accept invalid data"""
        size = 'MEDIUM'
        size_info = PrintSizeInfo.objects.get(size=PrintSize[size])
        shot_date = datetime.date(year=2000, month=1, day=1)
        photo = Photo.objects.create(image_id=1, image_location='photos',
                                     title='photo1', shot_date=shot_date,
                                     max_prints=10)
        # Bad size: "MEDIUM_"
        print_data = {'size_info__size': size + "_",
                      'photo__image_id': photo.image_id}
        serializer = PrintSerializer(data=print_data)

        self.assertFalse(serializer.is_valid())
        with self.assertRaises(AssertionError):
            serializer.save()
        created_print = Print.objects.filter(size_info=size_info, photo=photo,
                                             print_number=1)
        self.assertFalse(created_print.exists())
