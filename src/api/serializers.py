from rest_framework import serializers
from production.models import ProductTest, Cameraset

class ProductTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTest
        fields = ["id","test"]

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cameraset
        fields = [          
            'camera_name',
            'camera_no',
            'camera_link',
            'camera_image',
            'camera_main',
            'camera_point1x',
            'camera_point1y',
            'camera_point2x',
            'camera_point2y',
            'camera_point3x', 
            'camera_point3y',
            'camera_point4x', 
            'camera_point4y', 
            'camera_overlay',
            'camera_detection',
            'camera_annotation',
        ]