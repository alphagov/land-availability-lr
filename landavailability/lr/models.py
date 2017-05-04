from django.contrib.gis.db import models


class LRPoly(models.Model):
    # Describes an instance of a Title/Polygon from Land Registry

    title = models.CharField(unique=True, max_length=100)
    insert = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1)
    geom = models.GeometryField(geography=True, spatial_index=True)


class Uprn(models.Model):
    # Describes an instance of a UPRN with a Title associated

    title = models.ForeignKey(LRPoly)
    uprn = models.CharField(unique=True, max_length=100)
