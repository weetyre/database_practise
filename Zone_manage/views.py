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

from .models import ParLot
from .models import House
from .models import InOut
from .models import Bill
from .models import Advice
from .models import Fix
from .models import Worker
from .models import Hoster


def hostjudge_repair(req):
    return render(req, "4hosts/judge_repair.html")


def hostgo_repair(req):
    return render(req, "4hosts/go_repair.html")


def hostssuggests(req):
    return render(req, "4hosts/suggests.html")


def post_suggestion(req):
    data = req.POST.get("suggestion")
    work_id = req.POST.get("work_id")
    worker = Worker.objects.all().filter(w_id=work_id)
    hoster = Hoster.objects.all().filter(hos_id=req.session.get("user_id"))
    Advice.objects.create(workid=worker, hoster=hoster, content_field=data, state=0)
    return render(req, '4hosts/suggests.html')


# 待处理------------------------------------------------------------------------------------------------------------------------
def post_go_repair(req):
    data = req.POST.get("go_repair")
    print(data)
    return render(req, '4hosts/go_repair.html')


def post_judge_repair(req):
    data = req.POST.get("judge_repair")
    work_id = req.POST.get("work_id")
    worker = Worker.objects.get(w_id=work_id)
    hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
    Advice.objects.create(workid=worker, hoster=hoster, content_field=data, state=0)
    return render(req, '4hosts/judge_repair.html')


def pays(req):
    hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
    bill = Bill.objects.get(hoster_id=hoster)
    print(bill)
    return render(req, '4hosts/pays.html', {"bill": bill})


def do_pay(req):
    hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
    bill = Bill.objects.get(hoster_id=hoster)
    bill.b_amount = 0
    bill.save()
    bill = Bill.objects.get(hoster_id=hoster)
    return HttpResponse("缴费成功")


def park_rent_show(req):
    # 从数据库里取出数据
    parks = ParLot.objects.all().filter(avi=1)
    # 将数据发送到前段页面
    return render(req, '4hosts/park_rent.html', {"parks": parks})


def rentPark(req):
    park_id = req.GET.get("park_id")
    park = ParLot.objects.get(par_id=park_id)
    park.avi = 0
    hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
    park.host = hoster
    park.save()
    return HttpResponse("租赁成功")


def park_buy_show(req):
    parks = ParLot.objects.all().filter(avi=1)
    # 将数据发送到前段页面
    return render(req, '4hosts/park_buy.html', {"parks": parks})


def buyPark(req):
    park_id = req.GET.get("park_id")
    park = ParLot.objects.get(par_id=park_id)
    park.avi = 0
    hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
    park.host = hoster
    park.save()

    return HttpResponse("购买成功")


def house_rent_show(req):
    # 从数据库里取出数据
    houses = House.objects.all().filter(avi=1)
    # 将数据发送到前段页面
    return render(req, '4hosts/house_rent.html', {"houses": houses})


def rentHouse(req):
    house_id = req.GET.get("house_id")
    print(house_id)
    house = House.objects.get(ho_id=house_id)
    house.avi = 0
    hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
    house.host = hoster
    house.save()
    return HttpResponse("租赁成功")


def house_buy_show(req):
    houses = House.objects.all().filter(avi=1)
    # 将数据发送到前段页面
    return render(req, '4hosts/house_buy.html', {"houses": houses})


def buyHouse(req):
    house_id = req.GET.get("house_id")
    print(house_id)
    house = House.objects.get(ho_id=house_id)
    house.avi = 0
    hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
    house.host = hoster
    house.save()
    return HttpResponse("购买成功")


def inout(req):
    host = Hoster.objects.get(hos_id=req.session.get("user_id"))
    print(host)
    inouts = InOut.objects.all().filter(hoster=host)
    return render(req, '4hosts/info_in_out.html', {"inouts": inouts})


def show_data(req):
    hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
    houses = House.objects.all().filter(host=hoster)
    parks = ParLot.objects.all().filter(host=hoster)
    return render(req, "4hosts/data.html", {"hoster": hoster, "houses": houses, "parks": parks})


def modify_data(req):
    hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
    hoster.hos_id = req.POST.get("hos_id")
    hoster.hos_name = req.POST.get("hos_name")
    hoster.sex = req.POST.get("sex")
    hoster.contact = req.POST.get("contact")
    hoster.save()
    hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
    houses = House.objects.all().filter(host=hoster)
    parks = ParLot.objects.all().filter(host=hoster)
    return render(req, "4hosts/data.html", {"hoster": hoster, "houses": houses, "parks": parks})


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
                    user = request.user
                    HN = user.username
                    hoster = models.Hoster.objects.get(hos_name=HN)
                    request.session["user_id"] = hoster.hos_id  # hosterid
                    return render(request, '4.html',
                                  {"userid": hoster.hos_id, "username": hoster.hos_name})  # hosterid hostername
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
                return render(request, '0.html', )
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

        worker = models.Worker.objects.filter(w_id=int(WD))
        hoster = models.Hoster.objects.filter(hos_id=int(HD))

        if worker.count()==0 or hoster.count()==0:
            error_message = 'workerid or hoster id not exists!'
            return render(request, 'fa_fo.html', {'user': user,'error':error_message})
        else:
            succeed_message = 'Success!'
            models.Bill.objects.create(b_name=BN,b_amount=int(BA),hoster_id=hoster[0],worker=worker[0])
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

        hoster = models.Hoster.objects.filter(hos_id=int(H_id))
        if  hoster.count()==0:
            error_message = 'hoster id not exists!'
            return render(request, 'fa_fo.html', {'user': user,'errors':error_message})
        else:
            hoster[0].bonus = int(Bonus)
            hoster[0].coupon_nam = Coupon
            hoster[0].save()
            succeed_message = 'Success!'
            return render(request, 'fa_fo.html', {'user': user,'sucs':succeed_message})





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
