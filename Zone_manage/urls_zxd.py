from django.urls import path
from . import views_zxd as views

urlpatterns = [
    path('business_administrator/index/', views.business_administrator_index, name='business_administrator_index'),
    path('business_administrator/mail/', views.business_administrator_mail, name='business_administrator_mail'),
    path('business_administrator/checkin/', views.business_administrator_checkin, name='business_administrator_checkin'),
    path('business_administrator/complaints/', views.business_administrator_complaints),
    path('business_administrator/parking/', views.business_administrator_parking),
    path('management_manager/index/', views.management_manager_index, name='management_manager_index'),
    path('management_manager/mail/', views.management_manager_mail),
    path('management_manager/checkin/', views.management_manager_checkin,name='management_manager_checkin'),
    path('management_manager/complaints/', views.management_manager_complaints),
    path('management_manager/parking/', views.management_manager_parking),
    path('hydropower_maintenance_worker/index/', views.hydropower_maintenance_worker_index, name='hydropower_maintenance_worker_index'),
    path('hydropower_maintenance_worker/mail/', views.hydropower_maintenance_worker_mail),
    path('hydropower_maintenance_worker/checkin/', views.hydropower_maintenance_worker_mail_checkin),
    path('hydropower_maintenance_worker/complaints/', views.hydropower_maintenance_worker_complaints),
    path('hydropower_maintenance_worker/baoxiao/', views.hydropower_maintenance_baoxiao),

    path('bussiness_park_handle/', views.bussiness_park_handle),
    path('bussiness_checkin_delete/', views.bussiness_checkin_delete),
    path('bussiness_checkin_detail/', views.bussiness_checkin_detail),
    path('bussiness_checkin_update/', views.bussiness_checkin_update),
    path('management_manager_advice_share/', views.management_manager_advice_share),

    path('management_manager_delete/', views.management_manager_delete),
    path('management_manager_detail/', views.management_manager_detail),
    path('management_manager_update/', views.management_manager_update),

    path('management_manager_advice_finish/', views.management_manager_advice_finish),
]