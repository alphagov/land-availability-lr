from .models import LRPoly, Uprn
from rest_framework import serializers


class LRPolySerializer(serializers.ModelSerializer):

    class Meta:
        model = LRPoly
        fields = ('title', 'insert', 'update', 'status', 'geom')


class UprnSerializer(serializers.ModelSerializer):
    title = LRPolySerializer()

    class Meta:
        model = Uprn
        fields = ('title', 'uprn')
