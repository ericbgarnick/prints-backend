from rest_framework.response import Response
from rest_framework.views import APIView

from prints.models import PrintSizeInfo
from prints.serializers import PrintSizeInfoSerializer


class PrintsMeta(APIView):
    """
    Return meta data about prints:
    "print_size_info": [
        {
            "size_name": <str>,
            "base_price_cents": <int>,
            "shipping_cost_cents": <int>
        }
    ]
    """
    def get(self, request):
        prints_meta_data = PrintSizeInfo.objects.all()\
            .order_by('base_price_cents')
        serializer = PrintSizeInfoSerializer(prints_meta_data, many=True)
        return Response(serializer.data)
