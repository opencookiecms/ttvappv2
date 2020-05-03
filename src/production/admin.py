from django.contrib import admin
from .models import Ttvproject, Ttvcell,Cctvgroup, Cameraset, Cctvline, InventoryProduct,Groupcell,ProductTest

admin.site.register(Ttvproject)
admin.site.register(Ttvcell)
admin.site.register(Cctvgroup)
admin.site.register(Cameraset)
admin.site.register(Cctvline)
admin.site.register(InventoryProduct)
admin.site.register(Groupcell)
admin.site.register(ProductTest)

# Register your models here.
