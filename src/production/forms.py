from django import forms

from .models import Ttvproject, Ttvcell, Groupcell, Cameraset, Cctvgroup, InventoryProduct

class AddProjectForm(forms.ModelForm):

    p_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Project Name'}))
    p_company = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Company Name'}))
    p_code = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Project Code'}))
    p_model = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Model'}))
    p_startdate = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Start Date'}))
    p_enddate = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'End Date'}))
    p_status = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Status'}))

    class Meta:
        model = Ttvproject
        fields = [
            'p_name',
            'p_company',
            'p_code',
            'p_model',
            'p_startdate',
            'p_enddate',
            'p_status'
        ]

class UpdateProjectForm(forms.ModelForm):

    p_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Project Name'}))
    p_company = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Company Name'}))
    p_code = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Project Code'}))
    p_model = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Model'}))
    p_startdate = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Start Date'}))
    p_enddate = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'End Date'}))
    p_status = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Status'}))

    class Meta:
        model = Ttvproject
        fields = [
            'p_name',
            'p_company',
            'p_code',
            'p_model',
            'p_startdate',
            'p_enddate',
            'p_status'
        ]

class CellForm(forms.ModelForm):

    lane_choice = (
        ('0','No Lane'),
        ('1','Lane 1'),
        ('2','Lane 2'),
        ('3','Lane 3'),
        ('4','Lane 4'),
        ('5','Lane 5')
    )

    cell_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Cell Name'}))
    cell_size = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Size of Cell'
    }))
    cell_lane = forms.ChoiceField(choices=lane_choice, required=False, widget=forms.Select(attrs={
        'class':'form-control','placholder':'Lane of Cell'
    }))
    cell_status = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Status Cell'
    }))
    cell_color = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Cell Color'
    }))
    cell_group = forms.ModelChoiceField(required=False, queryset=Groupcell.objects.all(),widget=forms.Select(attrs={
        'class':'form-control'}))
    cell_project = forms.ModelChoiceField(required=False, queryset=Ttvproject.objects.all(), widget=forms.Select(attrs={
        'class':'form-control'
    }))

    class Meta:
        model = Ttvcell
        fields = [
            'cell_name',
            'cell_size',
            'cell_lane',
            'cell_status',
            'cell_color',
            'cell_group',
            'cell_project'
        ]

class CameraForm(forms.ModelForm):

    camera_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Camera Name'}))
    camera_no = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Camera No','value':'0'
    }))
    camera_link = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Link of Camera'}))
    camera_image = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Camera Image'}))
    
    camera_main = forms.BooleanField(required=False)

    camera_point1x =forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Overlay Point x1','value':'0'
    }))
    camera_point1y =forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Overlay Point y1','value':'0'
    }))
    camera_point2x =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Overlay Point x2','value':'0'
    }))
    camera_point2y =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Overlay Point y2','value':'0'
    }))
    camera_point3x =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Overlay Point x3','value':'0'
    }))
    camera_point3y =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Overlay Point y3','value':'0'
    }))
    camera_point4x =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Overlay Point x4','value':'0'
    }))
    camera_point4y =  forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Overlay Point y4','value':'0'
    }))

    camera_overlay = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'1 or 0','value':'0'
    }))
    camera_detection = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'1 or 0','value':'0'
    }))
    camera_annotation = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'1 or 0','value':'0'
    }))

    camera_group = forms.ModelChoiceField(required=False, queryset=Cctvgroup.objects.all(), widget=forms.Select(attrs={
        'class':'form-control'
    }))
    camera_cells = forms.ModelChoiceField(required=False, queryset=Ttvcell.objects.all(), widget=forms.Select(attrs={
        'class':'form-control'
    }))
    camera_project = forms.ModelChoiceField(required=False, queryset=Ttvproject.objects.all(), widget=forms.Select(attrs={
        'class':'form-control'
    }))


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
            'camera_group',
            'camera_cells',
            'camera_project'
        ]

class CCTVSettingForm(forms.ModelForm):

    setting_choice = (
       ('0','Off'),
       ('1','On')
    )

    camera_overlay = forms.ChoiceField(choices=setting_choice, required=False, widget=forms.Select(attrs={
        'class':'form-control'
    }))
    camera_detection = forms.ChoiceField(choices=setting_choice, required=False, widget=forms.Select(attrs={
        'class':'form-control'
    }))
    camera_annotation = forms.ChoiceField(choices=setting_choice, required=False, widget=forms.Select(attrs={
        'class':'form-control'
    }))

    class Meta:
        model = Cameraset
        fields = [
            
            'camera_overlay',
            'camera_detection',
            'camera_annotation'
        ]

class InventoryForm(forms.ModelForm):

    product_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Product Name'}))
    product_transaction = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Product Transaction'})) 
    product_partno = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Part Number'}))
    product_desc =forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class':'form-control','placeholder':'Description of Product'})) 
    product_job =forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Job Number'}))
    product_unit = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Product Unit'}))
    product_photo = forms.ImageField(required=False)

    product_duration = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Duration of Product'}))
        
    product_location = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Location'}))
    
    class Meta:
        model = InventoryProduct
        fields = [
            'product_name',
            'product_transaction',
            'product_partno',
            'product_desc', 
            'product_job', 
            'product_unit',
            'product_photo',
            'product_duration', 
            'product_location'
        ]





