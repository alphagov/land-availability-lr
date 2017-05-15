from .models import Polygon, Uprn
from rest_framework import serializers


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Polygon
        fields = ('id')


class UprnSerializer(serializers.ModelSerializer):
    title = TitleSerializer()

    class Meta:
        model = Uprn
        fields = ('title', 'uprn')
