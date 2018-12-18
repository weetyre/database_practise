from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from .admin import UserCreationForm
from .forms import LoginForm, ChangeEmailForm, MyPasswordChangeForm
from .models import MyUser
from . import models


def index_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # if email is not found
            flag = 1
            user_model = MyUser.objects.all()
            for i in user_model:
                if i.email == email:
                    flag = 0

            if flag:
                error_message = 'email not found.'
                return render(request, 'login.html',
                              {'form': form, 'input_error': error_message, 'block_title': 'Login'})

            # user = MyUser.objects.get(email=email)
            user = auth.authenticate(email=email, password=password)
            # incorrect password
            if user is None:
                error_message = 'password is invalid.'
                return render(request, 'login.html',
                              {'form': form, 'input_error': error_message, 'block_title': 'Login'})

            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)

                type = user.type

                if type == 0:
                    return render(request, '0.html', )
                elif type == 1:
                    return render(request, '1.html', )
                elif type == 2:
                    return render(request, '2.html', )
                elif type == 3:
                    return HttpResponseRedirect('/security')
                elif type == 4:
                    return render(request, '4.html', )
                elif type == 5:
                    return HttpResponseRedirect('/treasurer')
                # Redirect to a success page.
            else:
                error_message = "Sorry, that's not a valid username or password"
                return render(request, 'login.html',
                              {'form': form, 'input_error': error_message, 'block_title': 'Login'})
    else:
        form = LoginForm()
    return render(request, 'login.html',
                  {'form': form, 'block_title': 'Login'})


def index_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        email_filter = MyUser.objects.filter(email=request.POST['email'])
        username_filter = MyUser.objects.filter(username=request.POST['username'])
        if len(email_filter) <= 0 and len(username_filter) <= 0:
            # form.save()
            username = request.POST['username']
            email = request.POST['email']
            sex = request.POST['sex']
            type = int(request.POST['type'])
            # password = make_password(form.cleaned_data['password'])
            MyUser.objects.create_user(username, email, sex, type, request.POST['password'])
            user = auth.authenticate(email=email, password=request.POST['password'])
            auth.login(request, user)

            sex_num = None

            #注册成功，创建相应用户表
            if sex == 'boy':
                sex_num ='1'
            else:
                sex_num ='0'


            if type == 0:
                return render(request, '0.html',)
            elif type == 1:
                return render(request, '1.html', )
            elif type == 2:
                return render(request, '2.html', )
            elif type == 3:
                models.Worker.objects.create(name=username,sex=sex_num,type = type)
                return HttpResponseRedirect('/security')
            elif type == 4:
                return render(request, '4.html', )
            elif type == 5:
                models.Worker.objects.create(name=username, sex=sex_num, type=type)
                return HttpResponseRedirect('/treasurer')

        else:
            if len(email_filter) > 0:
                error_msg1 = 'email already taken.'
                return render(request, 'register.html',
                              {'form': form, 'input_error': error_msg1, 'block_title': 'Register'})

            if len(username_filter) > 0:
                error_msg2 = 'username already taken.'
                return render(request, 'register.html',
                              {'form': form, 'input_error': error_msg2, 'block_title': 'Register'})

    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form, 'block_title': 'Register'})


def index_landingPage(request):
    # mainpage
    return render(request, 'landingpage.html')


@login_required
def index_profile(request):
    if request.method == 'GET':
        user = request.user
        # user = auth.authenticate(request)
        form1 = MyPasswordChangeForm(user=user)
        form2 = ChangeEmailForm()
        return render(request, 'settings_account.html',
                      {'user': user, 'form_change_psw': form1, 'form_change_email': form2})


@login_required
def account_psw_change(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(user=request.user, data=request.POST)
        h = form
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            form2 = ChangeEmailForm()

            msg = 'succeeded!'
            return render(request, 'settings_account.html',
                          {'user': request.user, 'form_change_psw': form,
                           'form_change_email': form2, 'success_msg1': msg})
        else:
            form2 = ChangeEmailForm()
            return render(request, 'settings_account.html',
                          {'user': request.user, 'form_change_psw': form, 'form_change_email': form2})


@login_required
def account_email_change(request):
    if request.method == 'POST':
        user = request.user
        email = request.POST['email']
        email_filter = MyUser.objects.filter(email=request.POST['email'])
        if len(email_filter) <= 0:
            user.email = email
            user.save()
            form1 = MyPasswordChangeForm(user=user)
            form2 = ChangeEmailForm()
            msg = 'succeeded!'
            return render(request, 'settings_account.html',
                          {'user': request.user, 'form_change_psw': form1,
                           'form_change_email': form2, 'success_msg2': msg})
        else:
            form1 = MyPasswordChangeForm(user=user)
            form2 = ChangeEmailForm()
            error_message = 'email already taken.'
            return render(request, 'settings_account.html',
                          {'user': user, 'form_change_psw': form1, 'form_change_email': form2,
                           'error_msg': error_message})


@login_required
def index_logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")


def myhome(request):
    return render(request, 'home_base.html')

@login_required
def mysecurity(request):
    if request.method == 'GET':
        user = request.user
        infos = models.AInfo.objects.all()
        advice = models.Advice.objects.all()
        len = advice.count()

        hosts_boy = models.Hoster.objects.filter(sex='1')
        hosts_girl = models.Hoster.objects.filter(sex='0')

        boy_sum = hosts_boy.count()
        girl_sum = hosts_girl.count()
        sum = boy_sum+girl_sum
        return render(request, '3.html', {'user': user,'info':infos,'advice':advice,'len':len,'boy_num':boy_sum,'girl_num':girl_sum,'total':sum})

@login_required
def s_ca(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'calendar.html', {'user': user})

@login_required
def s_char(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'chartjs.html', {'user': user})

@login_required
def s_form(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'form_validation.html', {'user': user})

    if request.method == 'POST':
        user = request.user
        Hname = request.POST['HostName']
        Wnumber = request.POST['WorkID']
        Hnumber = request.POST['HostID']
        phone = request.POST['phone']
        text = request.POST['textarea']

        worker = models.Worker.objects.filter(w_id=int(Wnumber))[0]
        hoster = models.Hoster.objects.filter(hos_id=int(Hnumber))[0]

        if worker==None or hoster==None:
            error_message = 'workerid or hoster id not exists!'
            return render(request, 'form_validation.html', {'user': user,'error':error_message})
        else:
            succeed_message = 'Success!'
            models.InOut.objects.create(guest_name=Hname, worker=worker, contact=int(phone), remark=text, hoster=hoster)
            return render(request, 'form_validation.html', {'user': user,'suc':succeed_message})


@login_required
def s_ta(request):
    if request.method == 'GET':
        user = request.user
        LOGS = models.InOut.objects.all()
        return render(request, 'tables_dynamic.html', {'user': user, 'LOGS':LOGS})

@login_required
def myfinance(request):
    if request.method == 'GET':
        user = request.user
        infos = models.AInfo.objects.all()
        advice = models.Advice.objects.all()
        len = advice.count()

        hosts_boy = models.Hoster.objects.filter(sex='1')
        hosts_girl = models.Hoster.objects.filter(sex='0')

        boy_sum = hosts_boy.count()
        girl_sum = hosts_girl.count()
        sum = boy_sum + girl_sum
        return render(request, '5.html', {'user': user,'info':infos,'advice':advice,'len':len,'boy_num':boy_sum,'girl_num':girl_sum,'total':sum})

@login_required
def f_ch(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'fa_ch.html', {'user': user})

@login_required
def f_fo(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'fa_fo.html', {'user': user})

    if request.method == 'POST':
        user = request.user
        BN = request.POST['BillN']
        BA = request.POST['BillA']
        HD = request.POST['HostID']
        WD = request.POST['WorkerId']

        worker = models.Worker.objects.filter(w_id=int(WD))[0]
        hoster = models.Hoster.objects.filter(hos_id=int(HD))[0]

        if worker==None or hoster==None:
            error_message = 'workerid or hoster id not exists!'
            return render(request, 'fa_fo.html', {'user': user,'error':error_message})
        else:
            succeed_message = 'Success!'
            models.Bill.objects.create(b_name=BN,b_amount=int(BA),hoster_id=hoster,worker=worker)
            return render(request, 'fa_fo.html', {'user': user,'suc':succeed_message})


@login_required
def f_fo_bonus(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'fa_fo.html', {'user': user})

    if request.method == 'POST':
        user = request.user
        H_id = request.POST['HosterId']
        Bonus = request.POST['Bonus']
        Coupon = request.POST['Coupon']

        hoster = models.Hoster.objects.filter(hos_id=int(H_id))[0]
        if  hoster==None:
            error_message = 'hoster id not exists!'
            return render(request, 'fa_fo.html', {'user': user,'error':error_message})
        else:
            hoster.bonus = int(Bonus)
            hoster.coupon_nam = Coupon
            hoster.save()
            succeed_message = 'Success!'
            return render(request, 'fa_fo.html', {'user': user,'suc':succeed_message})





@login_required
def f_ta(request):
    if request.method == 'GET':
        user = request.user
        BILLS = models.Bill.objects.all()#查询所有账单
        return render(request, 'fa_ta.html', {'user': user, 'BILLS': BILLS})

@login_required
def f_ca(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'fa_ca.html', {'user': user})