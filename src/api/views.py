from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import viewsets
from production.models import ProductTest
from .serializers import ProductTestSerializer


class ProductTestView(viewsets.ModelViewSet):
    queryset = ProductTest.objects.all()
    serializer_class = ProductTestSerializer

    
