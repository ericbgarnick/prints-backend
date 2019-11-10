from unittest import mock

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from prints.models import PrintSizeInfo
from prints.serializers import PrintSizeInfoSerializer
from prints.tests.helpers import create_print_size_info_data
from prints.views import PrintsMeta


class TestPrintsViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test data
        cls.test_data = create_print_size_info_data()

    @classmethod
    def tearDownClass(cls):
        PrintSizeInfo.objects.all().delete()
        super().tearDownClass()

    def test_get_prints_meta(self):
        """Assert the expected Response is created and returned"""
        prints_meta_data = PrintSizeInfo.objects.all() \
            .order_by('base_price_cents')
        serializer = PrintSizeInfoSerializer(prints_meta_data, many=True)

        factory = APIRequestFactory()
        request = factory.get('/prints/meta')

        views_response = 'prints.views.Response'
        with mock.patch(views_response) as response_mock:
            response = PrintsMeta().get(request)
            response_mock.assert_called_with(serializer.data)
            self.assertIsInstance(response, mock.MagicMock)
            self.assertEqual(response_mock._mock_name, 'Response')
