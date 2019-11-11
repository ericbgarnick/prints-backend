import json

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Catalog
from catalog.serializers import CatalogSerializer


class CatalogPhotos(APIView):
    """
    Return pages of photos in the latest catalog.
    Page size = 20
    Response format:
    {
        “title”: <str>,
        "publish_date": <date: YYYY-MM-DD>,
        “images”: [
            {
                "image_id": <int>,
                "title": <str>,
                "file_location": <str: path/to/file>,
                "num_prints": <int>,
                "shot_date": <date: YYYY-MM-DD>
            }
        ]
    }

    """
    paginator = PageNumberPagination()

    def get(self, request):
        catalog = Catalog.objects.all().order_by('publish_date').last()
        if catalog:
            page = self.paginator.paginate_queryset(catalog, request)
            serializer = CatalogSerializer(page)
            return self.paginator.get_paginated_response(serializer.data)
        else:
            return Response()
