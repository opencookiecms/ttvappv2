from pyimagesearch.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import threading
import argparse
import datetime
import imutils
import time
import cv2
from .cameraR import CameraStream
from .cameraM import CameraStreamMulti

import numpy as np
from django.templatetags.static import static
from .forms import AddProjectForm,UpdateProjectForm,CellForm,CameraForm,CCTVSettingForm,InventoryForm
from .models import Ttvproject,Ttvcell,Cctvgroup,Cameraset,Cctvline,InventoryProduct,Groupcell


def index(request):
    return render(request, 'dashboard.html')
    

def cctv_dashboard(request):
    context = {
        'title':'by group',
        'camcategory':Cctvgroup.objects.all(),
    } 
    return render(request, 'cctv_dashboard.html',context)

def cctv_cam(id):

    camera = Cameraset.objects.get(id=id)
    cl = camera.camera_link
    print(cl)

    return cl

def cctv_cap(id):

    cameraL = Cameraset.objects.get(id=id)
    cl = cameraL.camera_link
    
    return cl

def cctv_frame(cams_id):

    cam = cctv_cam(cams_id)
    #cap = cv2.VideoCapture(cam)
    cap = CameraStream(cam).start()
    sub = cv2.createBackgroundSubtractorMOG2()


    while cap:

        camera = Cameraset.objects.get(id=cams_id)
        frame = cap.read()
        frame = imutils.resize(frame, width=700)

        convert = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')

def cctv_frame_multi(cams_id):

    cam = cctv_cap(cams_id)
    #cap = cv2.VideoCapture(cam)
    cap = CameraStreamMulti(cam).start()
    sub = cv2.createBackgroundSubtractorMOG2()


    while cap:

        camera = Cameraset.objects.get(id=cams_id)
        frame = cap.read()
        frame = imutils.resize(frame, width=100)

        convert = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')
     


def cctv_groupimg(request,id):
    if request.method == 'GET':
        return StreamingHttpResponse(cctv_cap(id), content_type='multipart/x-mixed-replace; boundary=frame')
    

def cctv_group(request,id):
    if request.method == 'GET':
         return StreamingHttpResponse(cctv_frame(id), content_type='multipart/x-mixed-replace; boundary=frame')


def camera_list(request):
    return render(request, 'camera_list.html')


def login_view(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('cctv')
        else:
            messages.info(request,'Wrong username/password')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

        
def inventoryadd(request):
    posts = InventoryProduct.objects.all() 
    return render(request, 'inventoryin.html', {'posts': posts})

def singlecam(request, camera_id):
    
    obj = Cameraset.objects.get(id=camera_id)
    form = CCTVSettingForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()

    context = {
        'cameraset':Cameraset.objects.get(id=camera_id),
        'test' : 'testing',
        'form': form
    }

    return render(request, 'cam_indie.html',context)


def cctv_camera(request, group_name):

    contex = {
        'cameraset':Cameraset.objects.filter(camera_group=group_name),
        'title':'Camera Group :',
        'group':group_name   
    }

    return render(request, 'camerav2.html',contex)

def CctvCameraProject(request, projectid):

    context = {
       
    }

    return render(request,'cctv_project.html')

def Cameramanage(request):

    context = {
        'camera': Cameraset.objects.all()
    }
    return render(request,'manage-camera.html',context)

#inventory section page

def inventoryview(request):

    contex = {
        'inventory' : InventoryProduct.objects.all()
    }

    return render(request, 'inventory_list.html',contex)


def Addinventory(request):

    form = InventoryForm(request.POST or None, request.FILES or None)
    if form.is_valid():

        form.save()
        #form.InventoryForm()

    data = {
        'form':form
    }

    return render(request,'inventory_add.html', data)

def UpdateInventory(request, iid):
    obj = InventoryProduct.objects.get(id=iid)
    form = InventoryForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
    
    context = {
        'form':form
    }

    return render(request, 'inventory_update.html',context)

#end of inventory

def Cellgroup(request):

    context = {
        'cellgroup': Groupcell.objects.all()
    }

    return render(request, 'cellgroup.html',context)

def Celllist(request, groupid):
    
    data = {
        'title':Groupcell.objects.get(id=groupid),
        'row1': Ttvcell.objects.filter(cell_lane=1).filter(cell_group=groupid),
        'row2': Ttvcell.objects.filter(cell_lane=2).filter(cell_group=groupid),
        'row3': Ttvcell.objects.filter(cell_lane=3).filter(cell_group=groupid),
        'row4': Ttvcell.objects.filter(cell_lane=4).filter(cell_group=groupid)
    }
    

    return render(request, 'cell-list.html',data)

def Cellmanage(request):

    data = {
        'cell':Ttvcell.objects.all()
    }

    return render(request, 'cell_manage.html',data)

def Addproject(request):

    form = AddProjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = AddProjectForm()
   
    context = {
        'form' : form
    }

    return render(request, 'project_add.html',context)

def Addcell(request):
    form = CellForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = CellForm()

    data = {
        'form':form
    }

    return render(request, 'cell_add.html',data)

def Updatecell(request, cid):
    obj = Ttvcell.objects.get(id=cid)
    form = CellForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    
    context = {
        'form':form
    }

    return render(request, 'cell_update.html',context)

def Addcamera(request):
    form = CameraForm(request.POST or None)
    if form.is_valid():
        form.save()
        form. CameraForm()
    
    data = {
        'form':form
    }
    return render(request, 'camera_add.html',data)

def Updateproject(request, pid):
    obj = Ttvproject.objects.get(id=pid)
    form = UpdateProjectForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    
    context = {  
        'form' : form, 
    }

    return render(request, 'project_update.html',context)

def Updatecamera(request, cid):
    obj = Cameraset.objects.get(id=cid)
    form = CameraForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    
    data = {
        'form': form
    }

    return render(request, 'camera_edit.html',data)

def ProjectList(request):

    data = {
        'list':Ttvproject.objects.all(),
        'count': Ttvproject.objects.filter(p_status="In Progress").count()
    }
    return render(request, 'project_list.html',data)

def Cctvbyproject(request, ppid):

    data = {
        'cam':Cameraset.objects.filter(camera_project=ppid)
    }

    return render(request, 'camera_project.html',data)

























    
            
        

            
  
    
