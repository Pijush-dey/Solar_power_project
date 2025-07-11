# from appAdmin import views
# from django.urls import path
# from django.conf import settings
# # from storeApp.views import views as storeviews

# urlpatterns = [
#     path('', views.index,name="index"),
#     path('login', views.index,name="index"),
#     path('logout', views.logout,name="logout"),
#     path('register', views.register,name="register"),

#     path('dashboard', views.dashboard,name="admin_dashboard"),

#     path('get_employees_data', views.employees_data,name="get_employees_data"),
#     path('employees', views.employees,name="employees"),
#     path('employees/<int:id>/details/', views.employees_details,name="employees_details"),
#     path('employees/cart/<int:id>', views.employees_cart,name="employees_cart"),
#     path('get_employees_row', views.get_employees_row,name="get_employees_row"),
#     path('delete_employees', views.delete_employees,name="delete_employees"),
#     path('restore_employees', views.restore_employees,name="restore_employees"),
#     path('employees/log', views.employees_log,name="employees_log"),
#     path('employee_export_csv', views.employee_export_csv,name="employee_export_csv"),

#     path('stores', views.stores,name="stores"),
#     path('get_store_row', views.get_store_row,name="get_store_row"),
#     path('delete_store', views.delete_store,name="delete_store"),
#     path('stores/log', views.stores_log,name="stores_log"),
#     path('restore_stores', views.restore_stores,name="restore_stores"),
#     path('store_export_csv', views.store_export_csv,name="store_export_csv"),
#     path('store_upload_csv', views.store_upload_csv,name="store_upload_csv"),
    
#     path('products/details/<int:id>', views.productdetail,name="adminproductdetail"),
#     path('products', views.products,name="admin_products"),
#     path('get_product_subcategory', views.product_subcategory,name="get_product_subcategory"),
#     path('get_product_row', views.get_product_row,name="get_product_row"),
#     # path('get_products_image', storeviews.get_products_image,name="get_products_image"),

#     path('orders', views.orders,name="orders"),
#     path('orders/details/<int:id>', views.get_order_row,name="get_order_row"),
#     path('orders_data', views.orders_data,name="orders_data"),

#     path('products/size-master', views.product_size_master,name="product_size_master"),
#     path('size_master_data', views.size_master_data,name="size_master_data"),
#     path('get_size_master_row', views.get_size_master_row,name="get_size_master_row"),
#     path('delete_size_master', views.delete_size_master,name="delete_size_master"),
#     path('size_master_upload_csv', views.size_master_upload_csv,name="size_master_upload_csv"),
    
#     path('profile', views.profile,name="admin_profile"),
# ]