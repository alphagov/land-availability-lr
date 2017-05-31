from django.contrib.gis.db import models


class Title(models.Model):
    # Describes an instance of a Title from Land Registry
    id = models.CharField(unique=True, primary_key=True, max_length=20)
    # polygon_set
    # uprn_set


class Polygon(models.Model):
    # Describes an instance of a Polygon from Land Registry, which is
    # associated with a Title.

    id = models.IntegerField(unique=True, primary_key=True)
    title = models.ForeignKey(Title, related_name='polygons')
    insert = models.DateTimeField()
    update = models.DateTimeField()
    status = models.CharField(max_length=1)
    geom = models.GeometryField(geography=True, spatial_index=True)


class Uprn(models.Model):
    # Describes an instance of a UPRN with Title(s) associated

    titles = models.ManyToManyField(Title, related_name='uprns')
    uprn = models.CharField(unique=True, max_length=100)
