from rest_framework import serializers
from production.models import ProductTest

class ProductTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTest
        fields = ['id', 'test']