from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.models import Country, City
from core.api.serializers import OutputCountrySerializer, OutputCitySerializer


@api_view(("GET",))
def list_countries(request):
    countries = Country.objects.all().order_by('name')
    serializer = OutputCountrySerializer(countries, many=True)
    return Response(serializer.data)


@api_view(("GET",))
def list_cities(request):
    code = request.query_params.get('code', None)
    country = request.query_params.get('country', None)

    if code is None or country is None:
        context = {
            'city': ['code and country name are required.']
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    cities = City.objects.only('name').filter(
        country__code=code, country__name=country).order_by('name').all()
    serializer = OutputCitySerializer(cities, many=True)

    if len(serializer.data) == 0:
        context = {
            'city': ['cities were not found.']
        }
        return Response(context, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.data)
