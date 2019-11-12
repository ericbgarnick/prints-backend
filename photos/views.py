from django.core.handlers.wsgi import WSGIRequest
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from photos.models import Photo
from photos.serializers import PhotoSerializer


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
    Paginates response format:
    {
        "count": <int (total number of records available)>,
        "next": <str (url for next page, or null)>,
        "previous": <str (url for previous page, or null)>
        “images”: [
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

    def get(self, request: WSGIRequest):
        photos = Photo.objects.all().order_by('-shot_date')
        if request.GET.get('page'):
            page = self.paginator.paginate_queryset(photos, request)
            serializer = PhotoSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        else:
            serializer = PhotoSerializer(photos, many=True)
            return Response(serializer.data)
