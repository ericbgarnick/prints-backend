from django.core.handlers.wsgi import WSGIRequest
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.models import Photo
from photos.serializers import PhotoSerializer
from photos.utils import OrderBy, ordered_photos


class PhotoCatalog(APIView):
    """
    Return all available photos, optionally paginated.
    Pagination page size: 20
    Default response format:
    [
        {
            "image_id": <int>,
            "title": <str>,
            "file_location": <str: path/to/file>,
            "num_prints": <int>,
            "shot_date": <date: YYYY-MM-DD>
        }
    ]
    Paginated response format:
    {
        "count": <int (total number of records available)>,
        "next": <str (url for next page, or null)>,
        "previous": <str (url for previous page, or null)>
        "results": [
            {
                "image_id": <int>,
                "title": <str>,
                "file_location": <str: /relative/path/to/file>,
                "max_prints": <int>,
                "shot_date": <date: YYYY-MM-DD>
            }
        ]
    }

    """
    paginator = PageNumberPagination()

    DEFAULT_ORDER = OrderBy.SHOT_DATE.value

    def get(self, request: WSGIRequest):
        order_by = request.GET.get('order_by', self.DEFAULT_ORDER)
        photos = ordered_photos(order_by)
        if request.GET.get('page'):
            page = self.paginator.paginate_queryset(photos, request)
            serializer = PhotoSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        else:
            serializer = PhotoSerializer(photos, many=True)
            return Response(serializer.data)
