from django.urls import path
from . import views_zxd as views

urlpatterns = [
    path('business_administrator/index/', views.business_administrator_index),
    path('business_administrator/mail/', views.business_administrator_mail),
    path('business_administrator/checkin/', views.business_administrator_checkin),
    path('business_administrator/complaints/', views.business_administrator_complaints),
    path('business_administrator/parking/', views.business_administrator_parking),
]