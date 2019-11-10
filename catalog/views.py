from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView


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
        prints_meta_data = PrintSizeInfo.objects.all() \
            .order_by('base_price_cents')
        page = self.paginator.paginate_queryset(prints_meta_data, request)
        serializer = PrintSizeInfoSerializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)
