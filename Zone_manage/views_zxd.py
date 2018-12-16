from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from .admin import UserCreationForm

# Create your views here.


def homepage(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        return redirect('app_1:page')


def business_administrator_index(request):
     return render(request, 'templates_zxd/Business_Administrator/index.html')


def business_administrator_mail(request):
    return render(request, 'templates_zxd/Business_Administrator/mail.html')


def business_administrator_checkin(request):
    return render(request, 'templates_zxd/Business_Administrator/checkin.html')


def business_administrator_complaints(request):
    return render(request, 'templates_zxd/Business_Administrator/complaints.html')


def business_administrator_parking(request):
    return render(request, 'templates_zxd/Business_Administrator/parking.html')




