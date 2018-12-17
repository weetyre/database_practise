from django.urls import path
from . import views

urlpatterns = [
    path(r'post_suggestion/', views.post_suggestion),
    path(r'post_judge_repair/', views.post_judge_repair),
    path(r'post_go_repair/', views.post_go_repair),
    path(r'pays/', views.pays),
    path(r'do_pay/', views.do_pay),
    path(r'park_rent/', views.park_rent_show),
    path(r'rentPark/', views.rentPark),
    path(r'park_buy/', views.park_buy_show),
    path(r'buyPark/', views.buyPark),
    path(r'house_rent/', views.house_rent_show),
    path(r'rentHouse/', views.rentHouse),
    path(r'house_buy/', views.house_buy_show),
    path(r'buyHouse/', views.buyHouse),
    path(r'info_in_out/', views.inout),







    path('login', views.index_login, name='login'),
    path('', views.index_landingPage),
    path('profile', views.index_profile, name='profile'),
    path('register', views.index_register, name='register'),
    path('logout', views.index_logout, name='logout'),
    path('account/change_psw', views.account_psw_change, name='change_psw'),
    path('account/change_email', views.account_email_change),
    path('home', views.myhome),
    path('security', views.mysecurity),
    path('treasurer', views.myfinance),
    path('char', views.s_char),
    path('form', views.s_form),
    path('table', views.s_ta),
    path('ca', views.s_ca),

    path('fa_fos', views.f_fo_bonus),
    path('fa_ch', views.f_ch),
    path('fa_fo', views.f_fo),
    path('fa_ta', views.f_ta),
    path('fa_ca', views.f_ca),
    path('home', views.myhome),
]