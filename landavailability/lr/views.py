from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Uprn, Polygon
from .serializers import (
    UprnSerializer, PolygonCreationSerializer, UprnCreationSerializer)


class UprnDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Uprn.objects.all()
    serializer_class = UprnSerializer
    lookup_field = 'uprn'
    lookup_url_kwarg = 'uprn'


class PolygonCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = PolygonCreationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def polygons_from_point(request):
    try:
        lat = float(request.GET.get('lat', 0))
        long_ = float(request.GET.get('long', 0))
    except ValueError:
        return Response('parameters must be numbers',
                        status=status.HTTP_400_BAD_REQUEST)
    results = []
    # 'point in polygon' query e.g.
    # SELECT title_id FROM lr_polygon
    # WHERE ST_Intersects(ST_GeometryFromText(
    #     'POINT(0.1295208 52.2348256)'), geom);
    query = "SELECT id from lr_polygon " \
        "WHERE ST_Intersects(ST_GeometryFromText(" \
        "'POINT({long} {lat})'), geom);".format(lat=lat, long=long_)
    for polygon in Polygon.objects.raw(query):
        results.append(dict(
            polygon=polygon.geom.geojson,
            title=polygon.title_id,
            uprns=[uprn.uprn for uprn in polygon.title.uprns.all()],
        ))
    return Response(results)


class UprnCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = UprnCreationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
