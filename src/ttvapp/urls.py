from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


from production.views import (
    index,
    cctv_dashboard,
    cctv_camera,
    Cameramanage,
    singlecam,
    Updatecamera,
    cctv_group,
    Addproject,
    ProjectList,
    Updateproject,
    Addcamera,
    Cellgroup,
    Addcell,
    Celllist,
    Cellmanage,
    Updatecell,
    Cctvbyproject,
    cctv_all
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('',index),
    path('cctv',cctv_dashboard, name='cctv'), #cctv_dashboard.html
    path('camera/<int:group_name>/',cctv_camera, name='camera'),#camerav2.html
    path('camera_list', Cameramanage, name="camera_list"),#manage_camera.html
    path('singlecam/<int:camera_id>/', singlecam, name='singlecam'),#cam_indie.html
    path('cctv_group/<int:id>', cctv_group, name="cctv_group"),#cmaera link
    path('cctv_groupimg/<int:id>', cctv_group, name="cctv_groupimg"),#camera link multi
    path('add-project', Addproject, name='add-project'),
    path('project-list',ProjectList, name='project-list'),#project_list
    path('update-project/<int:pid>/',Updateproject, name='update-project'),
    path('camera-add', Addcamera, name='camera-add'),
    path('cell-group',Cellgroup, name='cell-group'),#cellgroup
    path('cell-list/<int:groupid>/', Celllist, name='cell-list'),
    path('add-cell', Addcell, name='add-cell'),#cell-list.html
    path('cell-manage',Cellmanage, name='cell-manage'),
    path('update-cell/<int:cid>/',Updatecell, name='update-cell'),
    path('camera-edit/<int:cid>/',Updatecamera, name='camera-edit'),
    path('cctv_all', cctv_all, name='cctv_all'),

    path('cameraproject/<int:ppid>/', Cctvbyproject, name='cameraproject'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

