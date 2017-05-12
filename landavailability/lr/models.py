from django.contrib.gis.db import models


class LRPoly(models.Model):
    # Describes an instance of a Polygon from Land Registry, which is
    # associated with a Title.

    lrid = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    insert = models.DateTimeField()
    update = models.DateTimeField()
    status = models.CharField(max_length=1)
    geom = models.GeometryField(geography=True, spatial_index=True)


class Uprn(models.Model):
    # Describes an instance of a UPRN with a Title associated

    lrpoly = models.ForeignKey(LRPoly)  # one of them!
    title = models.CharField(max_length=100)
    uprn = models.CharField(unique=True, max_length=100)
