from rest_framework.response import Response
from rest_framework.views import APIView

from geospatial.models import US_STATE_ABBR, COUNTRY_NAMES


class GeoSpatialMeta(APIView):
    """
    Return meta data about prints:
    {
        "states": [<All US states>],
        "countries": [<All world countries>]
    }
    """
    def get(self, request):
        states = [pair[0] for pair in US_STATE_ABBR]
        countries = [pair[0] for pair in COUNTRY_NAMES]
        geo_data = {"states": states, "countries": countries}
        return Response(geo_data)
