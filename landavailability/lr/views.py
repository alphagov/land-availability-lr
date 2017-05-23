from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Uprn
from .serializers import UprnSerializer, PolygonCreationSerializer


class UprnDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Uprn.objects.all()
    serializer_class = UprnSerializer
    lookup_field = 'uprn'
    lookup_url_kwarg = 'uprn'


class PolygonCreateView(APIView):
    permission_classes = (IsAdminUser, )

    def post(self, request, format=None):
        serializer = PolygonCreationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
