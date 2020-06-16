from pyimagesearch.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User, auth
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseServerError
from django.views.decorators import gzip
import threading
import argparse
import datetime
import imutils
import time
import cv2
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
        'count': Cameraset.objects.filter(camera_group=7).count()
    } 
    return render(request, 'cctv_dashboard.html',context)

def cctv_cam(id):

    camera = Cameraset.objects.get(id=id)
    cl = camera.camera_link
    print(cl)
    
    return cl


def cctv_frame(cams_id):

    cam = cctv_cam(cams_id)
    cap = cv2.VideoCapture(cam)
    #fps = FPS().start()
    time.sleep(2.0)
    sub = cv2.createBackgroundSubtractorMOG2()

    while cap:

        camera = Cameraset.objects.get(id=cams_id)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        ret, frame = cap.read()# import image
        frame = imutils.resize(frame, width=700)
     
        if(camera.camera_overlay == 1):
           
            point1 = [camera.camera_point1x,camera.camera_point1y] # p1(x,y)..............p2(x,y)
            point2 = [camera.camera_point2x,camera.camera_point2y]
            point3 = [camera.camera_point3x,camera.camera_point3y]
            point4 = [camera.camera_point4x,camera.camera_point4y] #p4(x,y)................p3(x,y)

            #point1 = [10,10] # p1(x,y)..............p2(x,y)
            #point2 = [300,10]
            #point3 = [300,300]
            #point4 = [10,300] #p4(x,y)................p3(x,y)

            pts = np.array([point1,point2,point3,point4],np.int32)
            pts = pts.reshape((-1,1,2))
            #overlay = frame.copy(
            cv2.polylines(frame,[pts],True,(0,255,255))

            #cv2.addWeighted(overlay,0.3,frame,1-0.65,0,frame)


        if(camera.camera_annotation == 1):
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'test camera',(20,50), font, 1,(255,255,255),2,cv2.LINE_AA)
        if not ret: #if vid finish repeat
            frame = cv2.VideoCapture(cam)
            continue
        if ret:
            

            image = cv2.resize(frame, (0, 0), None, 1, 1)  # resize image

        
            if(camera.camera_detection == 1):

                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # converts image to gray
                fgmask = sub.apply(gray)  # uses the background subtraction
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # kernel to apply to the morphology
                closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
                opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
                dilation = cv2.dilate(opening, kernel)
                retvalbin, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)  # removes the shadows
                contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                minarea = 400
                maxarea = 50000
                for i in range(len(contours)): 
                    # cycles through all contours in current frame
                    if hierarchy[0, i, 3] == -1: 
                        # using hierarchy to only count parent contours (contours not within others)
                        area = cv2.contourArea(contours[i])  # area of contour
                        if minarea < area < maxarea: 
                            # area threshold for contour
                            # calculating centroids of contours
                            cnt = contours[i]
                            M = cv2.moments(cnt)
                            cx = int(M['m10'] / M['m00'])
                            cy = int(M['m01'] / M['m00'])
                            # gets bounding points of contour to create rectangle
                            # x,y is top left corner and w,h is width and height
                            x, y, w, h = cv2.boundingRect(cnt)
                            # creates a rectangle around contour
                            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            # Prints centroid text in order to double check later on
                            cv2.putText(image, str(cx) + "," + str(cy), (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX,.3, (0, 0, 255), 1)
                            cv2.drawMarker(image, 
                            (cx, cy), (0, 255, 255), cv2.MARKER_CROSS, markerSize=8, thickness=3,line_type=cv2.LINE_8)
                            #cv2.imshow("countours", image)

            frame = cv2.imencode('.png', image)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
            #fps.update()
    del(camera)
 

  
def cctv_groupimg(request,id):
    if request.method == 'GET':
        return StreamingHttpResponse(cctv_cap(id), content_type='multipart/x-mixed-replace; boundary=frame')
    
@gzip.gzip_page
def cctv_group(request,id):
    if request.method == 'GET':
        try:
            return StreamingHttpResponse(cctv_frame(id), content_type='multipart/x-mixed-replace; boundary=frame')
        except HttpResponseServerError as e:
            print("abrout")

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

def cctv_all(request):
    contex = {
        'cameraset':Cameraset.objects.filter(camera_group=7),
    }
    return render(request, 'camerav3.html',contex)

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

























    
            
        

            
  
    
