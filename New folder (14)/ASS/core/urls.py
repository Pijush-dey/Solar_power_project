# forms_app/urls.py

from django.urls import path
from core.views import *

urlpatterns = [
    path('project_create/', project_create, name='project_create'),
    path('step1/<str:slug>/', step1, name='step1'),
    # path('step1/<str:unique_id>/', views.upload_form, name='upload_form_with_id'),  # Accept unique_id as an argument
    path('step2/<str:slug>/', step2, name='step2'),
    # path('step2/<str:unique_id>/', views.upload_form, name='upload_form_with_id'),  # Accept unique_id as an argument
    path('step3/<str:slug>/', step3, name='step3'),
    # path('step3/<str:unique_id>/', views.upload_form, name='upload_form_with_id'),  # Accept unique_id as an argument
    # path('submit/', submit, name='submit'),
    path('save_session_data/', save_session_data, name="save_session_data"),
    path('invoice/<str:unique_id>/', invoice, name='invoice'),
    # path('save_devices/', save_devices, name='save_devices'),
    # path('save_session_data/', save_session_data, name='save_session_data'),
    path('upload_file/', upload_file, name='upload_file'),
    path('cancel_bill/', cancel_bill, name='cancel_bill'),
]