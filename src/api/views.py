from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import viewsets
from production.models import ProductTest, Cameraset
from .serializers import ProductTestSerializer, CameraSerializer


class ProductTestView(viewsets.ModelViewSet):
    queryset = ProductTest.objects.all()
    serializer_class = ProductTestSerializer

class CameraViewset(viewsets.ModelViewSet):
    queryset = Cameraset.objects.all()
    serializer_class = CameraSerializer

    
