from unittest import mock

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.test import TestCase
from rest_framework.serializers import Serializer
from rest_framework.test import APIRequestFactory
from typing import List, Union

from photos.models import Photo
from photos.serializers import PhotoSerializer
from photos.tests.helpers import create_photo_data
from photos.views import PhotoCatalog


class TestPrintsViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test data
        cls.test_data = create_photo_data()

    @classmethod
    def tearDownClass(cls):
        Photo.objects.all().delete()
        super().tearDownClass()

    def mock_response_check(self, mock_response_path: str,
                            request: WSGIRequest, serializer: Serializer):
        """Assert that the the Response at mock_response_path is called with
        serializer data and that the mock response is returned from the view"""
        with mock.patch(mock_response_path) as response_mock:
            response = PhotoCatalog().get(request)
            response_mock.assert_called_with(serializer.data)
            self.assertIsInstance(response, mock.MagicMock)

    def test_get_all_photos(self):
        """Assert the Response of all photos is created and returned"""
        photos = Photo.objects.all().order_by('-shot_date')
        serializer = PhotoSerializer(photos, many=True)

        factory = APIRequestFactory()
        request = factory.get('/photos')

        views_response = 'photos.views.Response'
        self.mock_response_check(views_response, request, serializer)

    # ----- Test PhotoCatalog paginated response ----- #
    def get_photos_page_check(self, photos: Union[List[Photo], QuerySet],
                              page: str):
        """Assert the Response of the indicated page of photos
        is correctly created and returned"""
        page_size = PhotoCatalog.paginator.page_size
        PhotoCatalog.paginator.page_size = 1

        serializer = PhotoSerializer(photos, many=True)

        factory = APIRequestFactory()
        request = factory.get(f'/photos?page={page}')
        # Update the request to behave like a DRF Request
        request.query_params = request.GET

        views_response = 'photos.views.PhotoCatalog.paginator.get_paginated_response'
        self.mock_response_check(views_response, request, serializer)

        PhotoCatalog.paginator.page_size = page_size

    def test_get_photos_first_page(self):
        """Assert the Response of the first page of photos
        is correctly created and returned"""
        photos = Photo.objects.all().order_by('-shot_date')[:1]
        self.get_photos_page_check(photos, '1')

    def test_get_photos_mid_page(self):
        """Assert the Response of a middle page of photos
        is correctly created and returned"""
        photos = Photo.objects.all().order_by('-shot_date')[1:2]
        self.get_photos_page_check(photos, '2')

    def test_get_photos_last_page(self):
        """Assert the Response of the first page of photos
        is correctly created and returned"""
        last_photo_idx = len(self.test_data) - 1
        photos = Photo.objects.all().order_by('-shot_date')[last_photo_idx:]
        self.get_photos_page_check(photos, 'last')
