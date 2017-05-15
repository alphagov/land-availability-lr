from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Uprn
from .serializers import UprnSerializer


class UprnDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Uprn.objects.all()
    serializer_class = UprnSerializer
    lookup_field = 'uprn'
    lookup_url_kwarg = 'uprn'
