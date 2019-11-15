from unittest import mock

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from geospatial.models import US_STATE_ABBR, COUNTRY_NAMES
from geospatial.views import GeoSpatialMeta


class TestGeospatialViews(TestCase):
    def test_get_geo_meta(self):
        """Assert the prints meta data Response is created and returned"""
        states = [pair[0] for pair in US_STATE_ABBR]
        countries = [pair[0] for pair in COUNTRY_NAMES]
        geo_data = {"states": states, "countries": countries}

        factory = APIRequestFactory()
        request = factory.get('/geospatial/meta')

        views_response = 'geospatial.views.Response'
        with mock.patch(views_response) as response_mock:
            response = GeoSpatialMeta().get(request)
            response_mock.assert_called_with(geo_data)
            self.assertIsInstance(response, mock.MagicMock)
