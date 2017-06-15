from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^uprns/(?P<uprn>[a-zA-Z0-9]+)/$',
        views.UprnDetailView.as_view(), name='uprn-detail'),
    url(
        r'^polygons/$',
        views.PolygonCreateView.as_view(), name='polygon-create'),
    url(
        r'^polygons-from-point$',
        views.polygons_from_point, name='polygons-from-point'),
    url(
        r'^uprns/$',
        views.UprnCreateView.as_view(), name='uprn-create'),
]
