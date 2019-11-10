from django.test import TestCase

from prints.models import PrintSize, PrintSizeInfo
from prints.serializers import PrintSizeInfoSerializer
from prints.tests.helpers import create_print_size_info_data


class TestPrintsSerializers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test data
        cls.test_data = create_print_size_info_data()

    @classmethod
    def tearDownClass(cls):
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
