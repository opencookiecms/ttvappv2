from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('apitest', views.ProductTestView)
router.register('cameraset', views.CameraViewset)

urlpatterns = [
    path('', include(router.urls))
]
