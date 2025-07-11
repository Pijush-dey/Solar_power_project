from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import os
from django.conf import settings
from login_history.models import LoginHistory
# from core.utils import generate_unique_id

# class UserProfile(models.Model):
#     USER_TYPE_CHOICES = (
#         ('admin', 'Admin'),
#         ('user', 'User'),
#     )
#     user       = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50)
#     last_name  = models.CharField(max_length=50)
#     email      = models.EmailField()
#     username   = models.CharField(max_length=150)
#     user_type  = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
#     file1 = models.FileField(upload_to='employees/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    username = models.CharField(max_length=150)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    file1 = models.FileField(upload_to='employees/', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"

class AdminPanelLoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    ip = models.CharField(max_length=39, blank=True, null=True)
    user_agent = models.TextField(blank=True)
    is_logged_in = models.BooleanField(default=True)
    action = models.CharField(max_length=10, choices=(('login', 'Login'), ('logout', 'Logout')))

    def __str__(self):
        return f"{self.user} - {self.action} - {self.date_time}"

class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | Login: {self.login_time} | Logout: {self.logout_time}"

# Model for Customer Details (Step 1)
class Customer(models.Model):
# Final version
    unique_id = models.CharField(max_length=6, editable=False, unique=True)
    # unique_id = models.CharField(max_length=6, unique=True, editable=False)  # Unique ID for each customer
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True, default="N/A")
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    adhar_number = models.CharField(max_length=12)
    project_name = models.CharField(max_length=200)
    project_type = models.CharField(max_length=50)
    usecase = models.CharField(max_length=50)
    formatted_total_load = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='In Progress')
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.unique_id

# Model for Appliances (Step 1)
class Appliance(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appliances')
    # user_id = models.CharField(max_length=100)
    device_name = models.CharField(max_length=100)
    load = models.FloatField()
    quantity = models.IntegerField()
    total = models.FloatField()

# Model for Main Items (Step 2)
class MainItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='main_items')
    # user_id = models.CharField(max_length=100)
    # device_type = models.CharField(max_length=50)  # e.g., panel, battery, psu
    device_name = models.CharField(max_length=150)
    hsn = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    discount = models.CharField(max_length=50)
    gst = models.CharField(max_length=50)
    discounted_price = models.CharField(max_length=50)
    final_value = models.CharField(max_length=50)

# Model for Installation Kit (Step 2)
class InstallationKit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='installation_kits')
    # user_id = models.CharField(max_length=100)
    device_name = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)
    discount = models.CharField(max_length=50)
    gst = models.CharField(max_length=50)
    discounted_price = models.CharField(max_length=50)
    final_value = models.CharField(max_length=50)

# Model for Maintenance Plan (Step 3)
class MaintenancePlan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='maintenance_plans')
    monthly_charge = models.FloatField()
    # user_id = models.CharField(max_length=100)
    # plan_type = models.CharField(max_length=50)  # e.g., Basic, Advanced, Premium

# class Document(models.Model):
#     project = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')
#     file_name = models.CharField(max_length=255)  # Custom file name
#     file = models.FileField(upload_to='documents/', null=True, default=None)  # File stored in the 'documents/' directory

class CustomerFile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='customerfiles')
#    unique_id = models.CharField(max_length=255, unique=True, editable=False)  # Unique ID for each customer
    # first_name = models.CharField(max_length=255)
    # adhar_number = models.CharField(max_length=15)  # Phone number as a unique identifier
    file1 = models.FileField(upload_to='uploads/', null=True, blank=True)
    file2 = models.FileField(upload_to='uploads/', null=True, blank=True)
    file3 = models.FileField(upload_to='uploads/', null=True, blank=True)
    file4 = models.FileField(upload_to='uploads/', null=True, blank=True)
    file5 = models.FileField(upload_to='uploads/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.adhar_number

    # def save(self, *args, **kwargs):
    #     # Generate a unique ID if it doesn't exist
    #     if not self.unique_id:
    #         self.unique_id = generate_unique_id()
    #     super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete files from the filesystem when the record is deleted."""
        if self.file1:
            file1_path = os.path.join(settings.MEDIA_ROOT, self.file1.name)
            if os.path.exists(file1_path):
                os.remove(file1_path)
        if self.file2:
            file2_path = os.path.join(settings.MEDIA_ROOT, self.file2.name)
            if os.path.exists(file2_path):
                os.remove(file2_path)
        if self.file3:
            file3_path = os.path.join(settings.MEDIA_ROOT, self.file3.name)
            if os.path.exists(file3_path):
                os.remove(file3_path)
        if self.file4:
            file4_path = os.path.join(settings.MEDIA_ROOT, self.file4.name)
            if os.path.exists(file4_path):
                os.remove(file4_path)
        if self.file5:
            file5_path = os.path.join(settings.MEDIA_ROOT, self.file5.name)
            if os.path.exists(file5_path):
                os.remove(file5_path)
        super().delete(*args, **kwargs)

    def delete_file1(self):
        """Delete file1 from the filesystem and database."""
        if self.file1:
            file1_path = os.path.join(settings.MEDIA_ROOT, self.file1.name)
            if os.path.exists(file1_path):
                os.remove(file1_path)
            self.file1 = None  # Clear file1 field in the database
            self.save()

    def delete_file2(self):
        """Delete file2 from the filesystem and database."""
        if self.file2:
            file2_path = os.path.join(settings.MEDIA_ROOT, self.file2.name)
            if os.path.exists(file2_path):
                os.remove(file2_path)
            self.file2 = None  # Clear file2 field in the database
            self.save()

    def delete_file3(self):
        """Delete file3 from the filesystem and database."""
        if self.file3:
            file3_path = os.path.join(settings.MEDIA_ROOT, self.file3.name)
            if os.path.exists(file3_path):
                os.remove(file3_path)
            self.file3 = None  # Clear file3 field in the database
            self.save()

    def delete_file4(self):
        """Delete file4 from the filesystem and database."""
        if self.file4:
            file4_path = os.path.join(settings.MEDIA_ROOT, self.file4.name)
            if os.path.exists(file4_path):
                os.remove(file4_path)
            self.file4 = None  # Clear file4 field in the database
            self.save()

    def delete_file5(self):
        """Delete file5 from the filesystem and database."""
        if self.file5:
            file5_path = os.path.join(settings.MEDIA_ROOT, self.file5.name)
            if os.path.exists(file5_path):
                os.remove(file5_path)
            self.file5 = None  # Clear file5 field in the database
            self.save()            

class Project(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='projects')
    project_name=models.CharField(max_length=255) 
    project_type=models.CharField(max_length=255) 
    usecase=models.CharField(max_length=255)  

class Payment(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    total_main_items=models.CharField(max_length=255) 
    total_kit_amount=models.CharField(max_length=255) 
    installation_charges=models.CharField(max_length=255) 
    logistic_charges=models.CharField(max_length=255)
    summaryTotal=models.CharField(max_length=255)
    advance_payment=models.CharField(max_length=255) 
    remaining_payment=models.CharField(max_length=255) 

class Solar_battery(models.Model):
    name=models.CharField(max_length=255)
    hsn=models.CharField(max_length=255)
    price=models.IntegerField()

class Solar_panel(models.Model):
    name=models.CharField(max_length=255)
    hsn=models.CharField(max_length=255)
    price=models.IntegerField()

class Solar_psu(models.Model):
    name=models.CharField(max_length=255)
    hsn=models.CharField(max_length=255)
    price=models.IntegerField()


# class ProductSizeMaster(models.Model):     
#     omament_cat   = models.CharField(default="",max_length=100)    
#     size_code     = models.CharField(max_length=256,default="",null=True)
#     from_range    = models.CharField(max_length=256,default="",null=True)
#     to_range      = models.CharField(max_length=256,default="",null=True)
#     # status        = models.IntegerField(_("active"),choices=Status.choices,default=1)
#     created_at    = models.DateTimeField(auto_now_add=True)
#     updated_at    = models.DateTimeField(auto_now_add=False,auto_now=True,blank=True,null=True)
#     deleted_at    = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)

#     class Meta:
#         unique_together = ('omament_cat', 'size_code')
#         db_table = "tbl_product_size_master"

# class Product(models.Model): 
#     CustomizDesignType = [
#         ('yes','Yes'),
#         ('no', 'No')
#     ]
#     design_number       = models.CharField(unique=True, default="",max_length=100)
#     omament_cat         = models.CharField(default="",max_length=100)
#     ornament_cat_name   = models.CharField(default="",max_length=500)
#     omament_subcat      = models.CharField(default="",max_length=100,blank=True)
#     ornament_subcat_name= models.CharField(default="",max_length=500,blank=True)
#     collection_code     = models.CharField(default="",max_length=100)
#     style_code          = models.CharField(default="",max_length=100)
#     theme_code          = models.CharField(default="",max_length=100)
#     item_type_code      = models.CharField(default="",max_length=100)
#     department          = models.CharField(default="",max_length=100)
#     receieving_warehouse= models.CharField(max_length=500,default="")
#     receieving_site     = models.CharField(max_length=500,default="")
#     approx_weight       = models.CharField(max_length=500,default="",blank=True,null=True) 
#     dia_weight          = models.CharField(max_length=500,default="",blank=True,null=True) 
#     metal_type          = models.CharField(max_length=500,default="",blank=True,null=True) 
#     design_name         = models.CharField(max_length=500,default="",blank=True,null=True) 
#     design_creation_date= models.DateField(default="",blank=True,null=True) 
#     customized_design   = models.CharField(max_length=10,default="no",choices=CustomizDesignType)
#     status              = models.CharField(max_length=500,default="")
#     shortage_number     = models.CharField(max_length=100,default="")
#     vendor_code         = models.CharField(max_length=100,default="")
#     created_at          = models.DateTimeField(auto_now_add=True)
#     updated_at          = models.DateTimeField(auto_now_add=False,auto_now=True,blank=True,null=True)
#     deleted_at          = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)

#     class Meta:
#         db_table = "tbl_product"

# class Product_purity(models.Model):  
#     product_id          = models.ForeignKey(Product,related_name='configpurity', on_delete=models.CASCADE,default="") 
#     pro_purity          = models.CharField(max_length=256,default="",null=True)
#     class Meta:
#         db_table = "tbl_product_purity"

# class Product_size(models.Model):  
#     product_id          = models.ForeignKey(Product,related_name='configsize', on_delete=models.CASCADE,default="") 
#     ornamentsize        = models.CharField(max_length=256,default="",null=True)
#     class Meta:
#         db_table = "tbl_product_size"

# class Order(models.Model):
#     store_code              = models.CharField(max_length=100,default="")
#     employee_id             = models.IntegerField(default="")
#     ref_id                  = models.CharField(max_length=100,default="")
#     requisition_no          = models.CharField(unique=True ,max_length=100,default="")
#     requisition_type        = models.CharField(max_length=100,default="")
#     requisition_order_type  = models.CharField(max_length=100,default="")
#     document_date           = models.DateField(default="")
#     expected_delivery_date  = models.DateField(default="")
#     ordering_warehouse      = models.CharField(max_length=500,default="")
#     ordering_site           = models.CharField(max_length=500,default="")
#     item_type_code          = models.CharField(max_length=100,default="")
#     department              = models.CharField(max_length=100,default="")
#     receieving_warehouse    = models.CharField(max_length=500,default="")
#     receieving_site         = models.CharField(max_length=500,default="")
#     sales_person_code       = models.CharField(max_length=100,default="")
#     description             = models.CharField(null=True,max_length=500,default="")
#     confirmation_date       = models.DateField(default="")
#     created_by              = models.IntegerField(default="")
#     status                  = models.IntegerField(choices=Status.choices,default=1)
#     created_at              = models.DateTimeField(auto_now_add=True)
#     updated_at              = models.DateTimeField(auto_now_add=False,auto_now=True,blank=True,null=True)
#     deleted_at              = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)

#     class Meta:
#         db_table = "tbl_order"

# class Order_products(models.Model):
#     order_id            = models.ForeignKey(Order, on_delete=models.CASCADE)
#     ornament_cat        = models.CharField(default="",max_length=100)
#     ornament_subcat     = models.CharField(default="",max_length=100)
#     product_id          = models.ForeignKey(Product, on_delete=models.CASCADE,default="")
#     product_design_num  = models.CharField(max_length=100,default="")
#     product_qty         = models.IntegerField(default=1)
#     product_img         = models.CharField(max_length=256,default="",null=True)
#     purity              = models.CharField(max_length=100,default="",null=True)    
#     size                = models.CharField(max_length=100,default="",null=True)            
#     approx_weight       = models.CharField(max_length=100,default="",null=True) 
#     dia_weight          = models.CharField(max_length=100,default="",null=True) 
#     remark              = models.CharField(max_length=100,default="",null=True) 
#     description         = models.CharField(max_length=100,default="",null=True)
#     order_number        = models.CharField(max_length=200,default="",blank=True)
#     line_rec_id         = models.CharField(max_length=200,default="",blank=True)
#     plan_id             = models.CharField(max_length=200,default="",blank=True)
#     ref_id              = models.CharField(max_length=200,default="",blank=True)
#     sy_no               = models.CharField(max_length=200,default="",blank=True)
#     item_number         = models.CharField(max_length=200,default="",blank=True)
#     mrp_branch          = models.CharField(max_length=200,default="",blank=True)
#     ref_line_number     = models.CharField(max_length=200,default="",blank=True)
#     created_at          = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         db_table = "tbl_order_products"

# class Wish_products(models.Model):
#     PRODUCT_TYPE = [
#         (0, 'normal'),
#         (1, 'material')
#     ]
#     store_code          = models.CharField(max_length=100,default="")
#     product_type        = models.IntegerField(default=0,choices=PRODUCT_TYPE)
#     ornament_cat        = models.CharField(default="",max_length=100)
#     ornament_subcat     = models.CharField(default="",max_length=100)
#     req_type_id         = models.IntegerField(default=0)
#     req_type_txt        = models.CharField(max_length=200,default="")
#     product_id          = models.IntegerField()
#     employee_id         = models.IntegerField()
#     pro_dept            = models.CharField(max_length=200,default="")
#     pro_itemtypecode    = models.CharField(max_length=200,default="")
#     pro_warehouse       = models.CharField(max_length=500,default="")
#     pro_site            = models.CharField(max_length=200,default="")
#     design_name         = models.CharField(max_length=500,default="",blank=True)
#     design_num          = models.CharField(max_length=500,default="")
#     product_qty         = models.IntegerField(default=1)
#     product_img         = models.CharField(max_length=256,default="",null=True)
#     purity              = models.CharField(max_length=100,default="",null=True)    
#     size                = models.CharField(max_length=100,default="",null=True)            
#     product_approx_weight = models.CharField(max_length=100,default="",null=True) 
#     approx_weight       = models.CharField(max_length=100,default="",null=True) 
#     dia_weight          = models.CharField(max_length=100,default="",null=True) 
#     remark              = models.CharField(max_length=100,default="",null=True) 
#     remark_txt          = models.CharField(max_length=100,default="",null=True) 
#     description         = models.CharField(max_length=100,default="",blank=True)
#     order_number        = models.CharField(max_length=200,default="",blank=True,null=True)
#     line_rec_id         = models.CharField(max_length=200,default="",blank=True,null=True)
#     plan_id             = models.CharField(max_length=200,default="",blank=True)
#     ref_id              = models.CharField(max_length=200,default="",blank=True)
#     sy_no               = models.CharField(max_length=200,default="",blank=True,null=True)
#     item_number         = models.CharField(max_length=200,default="",blank=True)
#     mrp_branch          = models.CharField(max_length=200,default="",blank=True)
#     ref_line_number     = models.CharField(max_length=200,default="",blank=True)
#     created_at          = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         db_table = "tbl_wish_products" 

# class Cart_products(models.Model):
#     PRODUCT_TYPE = [
#         (0, 'normal'),
#         (1, 'material')
#     ]
#     store_code          = models.CharField(max_length=100,default="")
#     product_type        = models.IntegerField(default=0,choices=PRODUCT_TYPE)
#     ornament_cat        = models.CharField(default="",max_length=100)
#     ornament_subcat     = models.CharField(default="",max_length=100)
#     req_type_id         = models.IntegerField(default=0)
#     req_type_txt        = models.CharField(max_length=200,default="")
#     product_id          = models.IntegerField()
#     employee_id         = models.IntegerField()
#     pro_dept            = models.CharField(max_length=200,default="")
#     pro_itemtypecode    = models.CharField(max_length=200,default="")
#     pro_warehouse       = models.CharField(max_length=500,default="")
#     pro_site            = models.CharField(max_length=200,default="")
#     design_name         = models.CharField(max_length=500,default="",blank=True)
#     design_num          = models.CharField(max_length=500,default="")
#     product_qty         = models.IntegerField(default=1)
#     product_img         = models.CharField(max_length=256,default="",null=True)
#     purity              = models.CharField(max_length=100,default="",null=True)    
#     size                = models.CharField(max_length=100,default="",null=True)            
#     product_approx_weight = models.CharField(max_length=100,default="",null=True) 
#     approx_weight       = models.CharField(max_length=100,default="",null=True) 
#     dia_weight          = models.CharField(max_length=100,default="",null=True) 
#     remark              = models.CharField(max_length=100,default="",null=True) 
#     remark_txt          = models.CharField(max_length=100,default="",null=True) 
#     description         = models.CharField(max_length=100,default="",blank=True)
#     order_number        = models.CharField(max_length=200,default="",blank=True,null=True)
#     line_rec_id         = models.CharField(max_length=200,default="",blank=True,null=True)
#     plan_id             = models.CharField(max_length=200,default="",blank=True)
#     ref_id              = models.CharField(max_length=200,default="",blank=True)
#     sy_no               = models.CharField(max_length=200,default="",blank=True,null=True)
#     item_number         = models.CharField(max_length=200,default="",blank=True)
#     mrp_branch          = models.CharField(max_length=200,default="",blank=True)
#     ref_line_number     = models.CharField(max_length=200,default="",blank=True)
#     created_at          = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         db_table = "tbl_cart_products"

# class Product_image(models.Model):  
#     product_id          = models.ForeignKey(Product, on_delete=models.CASCADE,default="")  
#     product_design_num  = models.CharField(unique=True, max_length=100,default="")
#     product_img         = models.CharField(max_length=256,default="",null=True)
#     class Meta:
#         db_table = "tbl_product_image"

# class API_Logs(models.Model):  
#     api_name   = models.CharField(max_length=200,default="")  
#     url        = models.CharField(max_length=500,default="")  
#     send_data  = models.JSONField(null=True)
#     response   = models.JSONField(null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         db_table = "tbl_api_logs"

# class MRP_product(models.Model): # this is separate table from original product table
#     approx_weight            = models.CharField(max_length=500,default="",blank=True) 
#     average_weight           = models.CharField(max_length=500,default="",blank=True) 
#     branch                   = models.CharField(max_length=500,default="") 
#     current_qty              = models.CharField(max_length=500,default="",blank=True) 
#     description              = models.CharField(max_length=500,default="",blank=True) 
#     design_number            = models.CharField(default="",max_length=100,blank=True)
#     from_size                = models.CharField(default="",max_length=100,blank=True)
#     gold_req                 = models.CharField(default="",max_length=100,blank=True)
#     item_type_code           = models.CharField(default="",max_length=100)
#     item_number              = models.CharField(default="",max_length=100)
#     lot_size_in_pcs          = models.CharField(default="",max_length=100,blank=True)
#     no_days                  = models.CharField(default="",max_length=100,blank=True)
#     no_of_lots               = models.CharField(default="",max_length=100,blank=True)
#     on_hands                 = models.CharField(default="",max_length=100,blank=True)
#     ornament_cat             = models.CharField(default="",max_length=100)
#     ornament_subcat          = models.CharField(default="",max_length=100)
#     pcs                      = models.CharField(default="",max_length=500,blank=True)
#     plan_id                  = models.CharField(default="",max_length=500,blank=True)
#     ref_id                   = models.CharField(default="",max_length=500,blank=True)
#     ref_line_id              = models.CharField(default="",max_length=500,blank=True)
#     ref_requisition_no       = models.CharField(default="",max_length=500,blank=True)
#     remarks                  = models.CharField(default="",max_length=500,blank=True)
#     req_pcs                  = models.CharField(default="",max_length=500,blank=True)
#     requisition_id           = models.CharField(default="",max_length=500,blank=True)
#     requisition_qty          = models.CharField(default="",max_length=500,blank=True)
#     status                   = models.CharField(max_length=500,default="",blank=True)
#     store_stock_level_rec_id = models.CharField(max_length=500,default="",blank=True)
#     subline_id               = models.CharField(max_length=500,default="",blank=True)
#     time_per_lot_min         = models.CharField(max_length=500,default="",blank=True)
#     to_size                  = models.CharField(max_length=500,default="",blank=True)
#     total_capacity_per_day   = models.CharField(max_length=500,default="",blank=True)
#     total_time               = models.CharField(max_length=500,default="",blank=True)
#     vendor_name              = models.CharField(max_length=500,default="",blank=True)
#     vendor_account           = models.CharField(max_length=500,default="",blank=True)
#     wt_from                  = models.CharField(max_length=500,default="",blank=True)
#     wt_to                    = models.CharField(max_length=500,default="",blank=True)
#     data_area_id             = models.CharField(max_length=500,default="",blank=True)
#     created_at               = models.DateTimeField(auto_now_add=True)
#     updated_at               = models.DateTimeField(auto_now_add=False,auto_now=True,blank=True,null=True)
#     deleted_at               = models.DateTimeField(auto_now_add=False,auto_now=False,blank=True,null=True)

#     class Meta:
#         db_table = "tbl_mrp_product"

# class MRP_Product_purity(models.Model):  
#     mrp_product_id  = models.ForeignKey(MRP_product,related_name='mrpconfigpurity', on_delete=models.CASCADE,default="") 
#     purity          = models.CharField(max_length=256,default="",null=True)
#     class Meta:
#         db_table = "tbl_mrp_product_purity"

# class MRP_Product_size(models.Model):  
#     mrp_product_id  = models.ForeignKey(MRP_product,related_name='mrpconfigsize', on_delete=models.CASCADE,default="") 
#     size_code       = models.CharField(max_length=256,default="",null=True)
#     class Meta:
#         db_table = "tbl_mrp_product_size"







# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.utils import timezone

# # Custom User Model
# class NewUser(AbstractUser):
#     USER_TYPE_CHOICES = (
#         (1, 'Admin'),
#         (2, 'Employee'),
#         (3, 'Store'),
#     )
    
#     usertype = models.IntegerField(choices=USER_TYPE_CHOICES)
#     status = models.BooleanField(default=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
    
#     class Meta:
#         db_table = 'tbl_user'

# # Employee Model
# class Employees(models.Model):
#     AGENT_TYPE_CHOICES = (
#         ('internal', 'Internal'),
#         ('external', 'External'),
#     )
    
#     user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='employee')
#     agent_code = models.CharField(max_length=50, unique=True)
#     agent_name = models.CharField(max_length=100)
#     agent_type = models.CharField(max_length=10, choices=AGENT_TYPE_CHOICES)
#     vendor_ac = models.CharField(max_length=50, blank=True, null=True)
#     store_id = models.CharField(max_length=50)
#     merchandiser = models.BooleanField(default=False)
#     ho_user = models.BooleanField(default=False)
#     admin_user = models.BooleanField(default=False)
#     bulk_ron = models.BooleanField(default=False)
#     ordering_warehouse = models.CharField(max_length=50, blank=True, null=True)
#     ordering_site = models.CharField(max_length=50, blank=True, null=True)
#     status = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#     updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
#     class Meta:
#         db_table = 'tbl_employees'

# # Store Model
# class Store(models.Model):
#     STORE_TYPE_CHOICES = (
#         ('normal store', 'Normal Store'),
#         ('franchisee store', 'Franchisee Store'),
#     )
    
#     user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='store')
#     store_code = models.CharField(max_length=50, unique=True)
#     store_name = models.CharField(max_length=100)
#     store_type = models.CharField(max_length=20, choices=STORE_TYPE_CHOICES)
#     store_address = models.TextField()
#     warehouse_code = models.CharField(max_length=50)
#     site_code = models.CharField(max_length=50)
#     store_contact_person_name = models.CharField(max_length=100)
#     store_contact_num = models.CharField(max_length=15)
#     store_email = models.EmailField()
#     status = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
    
#     class Meta:
#         db_table = 'tbl_store'

# # Product Model
# class Product(models.Model):
#     design_number = models.CharField(max_length=50, unique=True)
#     omament_cat = models.CharField(max_length=50)
#     ornament_cat_name = models.CharField(max_length=100)
#     omament_subcat = models.CharField(max_length=50)
#     ornament_subcat_name = models.CharField(max_length=100)
#     collection_code = models.CharField(max_length=50)
#     style_code = models.CharField(max_length=50)
#     theme_code = models.CharField(max_length=50)
#     item_type_code = models.CharField(max_length=50)
#     department = models.CharField(max_length=50)
#     vendor_code = models.CharField(max_length=50)
#     receieving_warehouse = models.CharField(max_length=50)
#     receieving_site = models.CharField(max_length=50)
#     approx_weight = models.DecimalField(max_digits=10, decimal_places=4)
#     dia_weight = models.DecimalField(max_digits=10, decimal_places=4)
#     design_creation_date = models.DateField()
#     product_image = models.ImageField(upload_to='products/', null=True, blank=True)
#     status = models.CharField(max_length=20, default='draft')  # draft, release, etc.
#     deleted_at = models.DateTimeField(null=True, blank=True)
    
#     class Meta:
#         db_table = 'tbl_product'

# # Product Purity Model
# class Product_purity(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purities')
#     pro_purity = models.CharField(max_length=20)
#     pro_rate = models.DecimalField(max_digits=10, decimal_places=2)
    
#     class Meta:
#         db_table = 'tbl_product_purity'

# # Product Size Model
# class Product_size(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
#     size_code = models.CharField(max_length=20)
#     size_qty = models.IntegerField()
    
#     class Meta:
#         db_table = 'tbl_product_size'

# # Product Size Master Model
# class ProductSizeMaster(models.Model):
#     omament_cat = models.CharField(max_length=50)
#     size_code = models.CharField(max_length=20)
#     from_range = models.DecimalField(max_digits=10, decimal_places=2)
#     to_range = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
    
#     class Meta:
#         db_table = 'tbl_product_size_master'
#         unique_together = ('omament_cat', 'size_code')

# # Order Model
# class Order(models.Model):
#     REQUISITION_TYPE_CHOICES = (
#         ('regular', 'Regular'),
#         ('special', 'Special'),
#     )
    
#     REQUISITION_ORDER_TYPE_CHOICES = (
#         ('new', 'New'),
#         ('exchange', 'Exchange'),
#         ('return', 'Return'),
#     )
    
#     STATUS_CHOICES = (
#         ('draft', 'Draft'),
#         ('submitted', 'Submitted'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#         ('completed', 'Completed'),
#     )
    
#     store_code = models.CharField(max_length=50)
#     employee = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True)
#     ref_id = models.CharField(max_length=50, blank=True, null=True)
#     requisition_no = models.CharField(max_length=20, unique=True)
#     requisition_type = models.CharField(max_length=10, choices=REQUISITION_TYPE_CHOICES)
#     requisition_order_type = models.CharField(max_length=10, choices=REQUISITION_ORDER_TYPE_CHOICES)
#     document_date = models.DateField()
#     expected_delivery_date = models.DateField()
#     ordering_warehouse = models.CharField(max_length=50)
#     ordering_site = models.CharField(max_length=50)
#     item_type_code = models.CharField(max_length=50)
#     department = models.CharField(max_length=50)
#     receieving_warehouse = models.CharField(max_length=50)
#     receieving_site = models.CharField(max_length=50)
#     sales_person_code = models.CharField(max_length=50)
#     description = models.TextField(blank=True, null=True)
#     confirmation_date = models.DateField()
#     created_by = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
    
#     class Meta:
#         db_table = 'tbl_order'

# # Order Products Model
# class Order_products(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     ornament_cat = models.CharField(max_length=50)
#     ornament_subcat = models.CharField(max_length=50)
#     product_design_num = models.CharField(max_length=50)
#     product_qty = models.IntegerField()
#     product_img = models.CharField(max_length=255, blank=True, null=True)
#     purity = models.CharField(max_length=20)
#     size = models.CharField(max_length=20)
#     approx_weight = models.DecimalField(max_digits=10, decimal_places=4)
#     dia_weight = models.DecimalField(max_digits=10, decimal_places=4)
#     remark = models.TextField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     order_number = models.CharField(max_length=50, blank=True, null=True)
#     line_rec_id = models.CharField(max_length=50, blank=True, null=True)
#     plan_id = models.CharField(max_length=50, blank=True, null=True)
#     ref_id = models.CharField(max_length=50, blank=True, null=True)
#     sy_no = models.CharField(max_length=50, blank=True, null=True)
#     item_number = models.CharField(max_length=50, blank=True, null=True)
#     mrp_branch = models.CharField(max_length=50, blank=True, null=True)
#     ref_line_number = models.CharField(max_length=50, blank=True, null=True)
    
#     class Meta:
#         db_table = 'tbl_order_products'

# # Cart Products Model
# class Cart_products(models.Model):
#     employee = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='cart_items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'tbl_cart_products'

# # Status Model (if needed for tracking status changes)
# class Status(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField(blank=True, null=True)
    
#     class Meta:
#         db_table = 'tbl_status'