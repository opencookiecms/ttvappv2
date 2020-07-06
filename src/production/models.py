from django.db import models
from django.urls import reverse

class Groupcell(models.Model):
    group_name = models.CharField(max_length=50, blank=True)
    group_no = models.IntegerField(default=0, blank=True)
    group_color = models.CharField(max_length=50, blank=True)
    

    def __str__(self):
        return self.group_name


class Ttvproject(models.Model):
  
    p_name = models.CharField(max_length=150, blank=True)
    p_company = models.CharField(max_length=100, blank=True)
    p_code = models.CharField(max_length=150, blank=True)
    p_model = models.CharField(max_length=150, blank=True)
    p_desc = models.CharField(max_length=150, blank=True)
    p_startdate = models.CharField(max_length=150, blank=True)
    p_enddate = models.CharField(max_length=150, blank=True)
    p_status = models.CharField(max_length=150, blank=True)
    p_type = models.CharField(max_length=150, blank=True)
    p_comp = models.CharField(max_length=150, blank=True)
    p_userid = models.IntegerField(default=0, blank=True)
    p_color = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.p_name
    
    def get_absolute_url(self):
        return reverse('cameraproject', kwargs={'ppid': self.id})


class Ttvcell(models.Model):
 
  
    cell_name = models.CharField(max_length=100, blank=True)
    cell_size = models.IntegerField(default=0, blank=True)
    cell_lane = models.IntegerField(default=0, blank=True)
    cell_status = models.CharField(max_length=10, blank=True)
    cell_color = models.CharField(max_length=10, blank=True)
    cell_group = models.ForeignKey(Groupcell, blank=True, null=True, on_delete = models.SET_NULL)
    cell_project = models.ForeignKey(Ttvproject,  blank=True, null=True, on_delete = models.SET_NULL)

    def get_absolute_url(self):
        return reverse("cellcamera", kwargs={"ppid": self.id})
    
    def __str__(self):
        return self.cell_name


class Cctvgroup(models.Model):

    cgroup_name = models.CharField(max_length=100, blank=True)
    cgroup_much = models.IntegerField(default=0, blank=True)
    cgroup_link = models.CharField(max_length=200, blank=True)
    cgroup_cardcolor = models.CharField(max_length=30, blank=True)
    cgroup_cell = models.ForeignKey(Ttvcell, blank=True, null=True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.cgroup_name

class Cameraset(models.Model):

    camera_name = models.CharField(max_length=50, blank=True)
    camera_no = models.IntegerField(default=0, blank=True)
    #test = models.CharField(max_length=200, blank=True)
    camera_link1 = models.CharField(max_length=200, blank=True)
    camera_link2 = models.CharField(max_length=200, blank=True)
 
    #camera_image = models.FileField(blank=True)
    #camera_main = models.BooleanField(blank=True, null=True)
    camera_main = models.CharField(max_length=200, blank=True)
    camera_slave = models.CharField(max_length=200, blank=True)
    
    camera_point1x = models.IntegerField(default=0, blank=True)
    camera_point1y = models.IntegerField(default=0, blank=True)
    camera_point2x =  models.IntegerField(default=0, blank=True)
    camera_point2y =  models.IntegerField(default=0, blank=True)
    camera_point3x =  models.IntegerField(default=0, blank=True)
    camera_point3y =  models.IntegerField(default=0, blank=True)
    camera_point4x =  models.IntegerField(default=0, blank=True)
    camera_point4y =  models.IntegerField(default=0, blank=True)

    camera_overlay = models.IntegerField(default=0, blank=True)
    camera_detection = models.IntegerField(default=0, blank=True)
    camera_annotation = models.IntegerField(default=0, blank=True)

    camera_group = models.ForeignKey(Cctvgroup, blank=True, null=True, on_delete = models.SET_NULL)
    #camera_cells = models.ForeignKey(Ttvcell, blank=True, null=True, on_delete = models.SET_NULL)
    #camera_project = models.ForeignKey(Ttvproject, blank=True, null=True, on_delete = models.SET_NULL)
    camera_cell_tag = models.ManyToManyField(Ttvcell)
    

    def __str__(self):
        return self.camera_name


class Cameraoverlay(models.Model):
    camera_point1x = models.IntegerField(default=0, blank=True)
    camera_point1y = models.IntegerField(default=0, blank=True)
    camera_point2x =  models.IntegerField(default=0, blank=True)
    camera_point2y =  models.IntegerField(default=0, blank=True)
    camera_point3x =  models.IntegerField(default=0, blank=True)
    camera_point3y =  models.IntegerField(default=0, blank=True)
    camera_point4x =  models.IntegerField(default=0, blank=True)
    camera_point4y =  models.IntegerField(default=0, blank=True)



class Cctvline(models.Model):

    camera_line_name = models.CharField(max_length=50, blank=True)
    point_one = models.CharField(max_length=50, blank=True)
    point_two = models.CharField(max_length=50, blank=True)
    point_three = models.CharField(max_length=50, blank=True)
    point_four = models.CharField(max_length=50, blank=True)
    camera_relate = models.ForeignKey(Cameraset, blank=True, null=True, on_delete = models.CASCADE)

    def __str__(self):
        return self.camera_line_name

class InventoryProduct(models.Model):
    product_name = models.CharField(max_length=150, blank=True)
    product_supplier = models.CharField(max_length=150, blank=True)
    product_ttvpn = models.CharField(max_length=50, blank=True)
    product_desc = models.TextField(blank=True) 
    product_qty = models.IntegerField(default=0, blank=True) 
    product_partno = models.CharField(max_length=150, blank=True)
    product_oum = models.CharField(max_length=20, blank=True)
    product_location = models.TextField(max_length=50, blank=True)
    product_jobno = models.CharField(max_length=150, blank=True)

    product_currency = models.CharField(max_length=10, blank=True)
    product_febexcrate= models.CharField(max_length=10, blank=True)
    product_totalprice = models.CharField(max_length=10, blank=True)
    product_pricefrom = models.CharField(max_length=30, blank=True)
    product_company = models.CharField(max_length=30, blank=True)
    product_ponumbers = models.CharField(max_length=30, blank=True)
    product_invoice = models.CharField(max_length=30, blank=True)
    product_invdate = models.CharField(max_length=30, blank=True)

    product_remarks = models.CharField(max_length=150, blank=True)
    product_photo = models.FileField(blank=True)
   

class ProductTest(models.Model):
    test = models.CharField(max_length=150, blank=True)




    
    
    
      
     
