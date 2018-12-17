from django.urls import path
from . import views

urlpatterns = [
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

    path('fa_ch', views.f_ch),
    path('fa_fo', views.f_fo),
    path('fa_ta', views.f_ta),
    path('fa_ca', views.f_ca),
]
