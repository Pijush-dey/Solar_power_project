from django.contrib import admin
from core.models import ModuleLoginHistory

@admin.register(ModuleLoginHistory)
class ModuleLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_time', 'ip', 'user_agent', 'is_logged_in', 'module')



# # Register your models here.

# from django.contrib import admin
# from django.utils.html import format_html
# from .models import Order
# from .utils import format_installation_kits

# class OrderAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 
#         'created_at', 
#         'total_sum_main_items', 
#         'total_sum_installation_items', 
#         'installation_kits_count', 
#         'installation_kits_display'
#     )
#     readonly_fields = ('installation_kits_display',)
#     search_fields = ('id',)  # Allows searching by ID

#     def installation_kits_display(self, obj):
#         return format_installation_kits(obj.installation_kits)

#     def installation_kits_count(self, obj):
#         """
#         Returns the count of installation kits in the order.
#         """
#         return len(obj.installation_kits)

#     installation_kits_display.short_description = "Installation Kits Details"
#     installation_kits_count.short_description = "Number of Installation Kits"

# # Register the Order model
# admin.site.register(Order, OrderAdmin)





# from django.contrib import admin
# from django.utils.html import format_html
# from .models import UserSubmission

# @admin.register(UserSubmission)
# class UserSubmissionAdmin(admin.ModelAdmin):
#     list_display = (
#         'first_name', 'last_name', 'appliance_count', 'view_files', 
#         'form2_field1', 'form2_field2', 'form3_field1', 'form3_field2', 'form3_field3',
#     )
    
#     def view_files(self, obj):
#         files = []
#         for i in range(1, 5):
#             file_field = getattr(obj, f'file_{i}', None)
#             if file_field:
#                 files.append(f'<a href="/media/{file_field}" target="_blank">File {i}</a>')
#         return format_html("<br>".join(files)) if files else "No files uploaded"
#     view_files.short_description = "Uploaded Files"

#     def appliance_count(self, obj):
#         return len(obj.appliances)
#     appliance_count.short_description = "Number of Appliances"

#     list_filter = ['first_name', 'last_name']
#     search_fields = ['first_name', 'last_name', 'form2_field1', 'form3_field1']






# from django_mongoengine.admin import DocumentAdmin
# from .models import StepTwoData

# # Register the main document in the admin interface
# class StepTwoDataAdmin(DocumentAdmin):
#     list_display = ('id', 'created_at', 'total_sum_main_items', 'total_sum_installation_items')
#     search_fields = ('id',)
#     readonly_fields = ('created_at',)

#     def installation_kit_count(self, obj):
#         return len(obj.installation_kits)
#     installation_kit_count.short_description = "Number of Installation Kits"

# admin.site.register(StepTwoData, StepTwoDataAdmin)
