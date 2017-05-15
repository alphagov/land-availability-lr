from .models import Polygon, Uprn, Title
from rest_framework import serializers


class PolygonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Polygon
        fields = ('id', 'insert', 'update', 'status', 'geom')


class TitleSerializer(serializers.ModelSerializer):
    polygons = PolygonSerializer(many=True, required=False)

    class Meta:
        model = Title
        fields = ('id', 'polygons')


class UprnSerializer(serializers.ModelSerializer):
    title = TitleSerializer()

    class Meta:
        model = Uprn
        fields = ('uprn', 'title')
