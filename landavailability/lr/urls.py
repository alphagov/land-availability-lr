from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^lr/(?P<uprn>[a-zA-Z0-9]+)/$',
        views.UprnDetailView.as_view(), name='uprn-detail'),
    url(
        r'^polygons/$',
        views.PolygonCreateView.as_view(), name='polygon-create'),
]
