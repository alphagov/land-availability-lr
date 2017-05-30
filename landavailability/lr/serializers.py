from .models import Polygon, Uprn, Title
from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
import json
from datetime import datetime


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


class PolygonCreationSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    srid = serializers.IntegerField(write_only=True)

    class Meta:
        model = Polygon
        fields = ('id', 'insert', 'update', 'status', 'geom', 'title', 'srid')

    def create(self, validated_data):
        title_id = validated_data['title']

        try:
            title = Title.objects.get(id=title_id)
        except Title.DoesNotExist:
            title = Title(id=title_id)
            title.save()

        try:
            polygon = Polygon.objects.get(id=validated_data.get('id'))
        except Polygon.DoesNotExist:
            polygon = Polygon(id=validated_data.get('id'))

        polygon.title = title
        polygon.geom = GEOSGeometry(
            validated_data.get('geom').geojson,
            srid=validated_data.get('srid'))
        polygon.insert = validated_data.get('insert')
        polygon.update = validated_data.get('update')
        polygon.status = validated_data.get('status')

        polygon.save()
        return polygon


class UprnCreationSerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = Uprn
        fields = ('uprn', 'title')

    def create(self, validated_data):
        uprn_id = validated_data.get('uprn')

        title = Title.objects.get(id=validated_data.get('title'))

        try:
            uprn = Uprn.objects.get(uprn=uprn_id)
        except Uprn.DoesNotExist:
            uprn = Uprn(uprn=uprn_id)

        uprn.title = title

        uprn.save()
        return uprn

    def validate_title(self, value):
        if Title.objects.filter(id=value).count() == 0:
            raise serializers.ValidationError(
                'Title {0} does not exist'.format(value))
        return value
