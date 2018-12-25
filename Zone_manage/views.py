from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect

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
from .models import Fix_Service


def show_daipingjia(req):
    hoster = Hoster.objects.get(hos_id=int(req.session.get("user_id")))
    print(hoster)
    services = Advice.objects.all().filter(type_field=1,state=1,hoster=hoster)
    print(services)
    return render(req, '4hosts/show_daipingjia.html', {"services": services})


def unRentHouse(req):
    ho_id = req.GET.get("ho_id")
    house = House.objects.get(ho_id=int(ho_id))
    house.avi = 0
    house.host_id = None
    house.save()
    return HttpResponse("退租成功")


def unRentPark(req):
    par_id = req.GET.get("par_id")
    park = ParLot.objects.get(par_id = int(par_id))
    park.avi = 0
    park.host_id = None
    park.save()
    return HttpResponse("退租成功")

def hostjudge_repair(req):
    work_id = req.GET.get("workid")
    service_id = req.GET.get("serviceid")
    print("workid = ",work_id)
    print(type(work_id))
    return render(req, "4hosts/judge_repair.html",{"work_id":work_id,"serviceid":service_id})


def hostgo_repair(req):
    return render(req, "4hosts/go_repair.html")

from .models import Uses
from .models import AInfo
def usage(req):
    try:
        a_infos = AInfo.objects.all()

        hoster = Hoster.objects.get(hos_id=int(req.session.get("user_id")))
        uses = Uses.objects.all().filter(hoster=hoster.hos_id)
        return render(req,"4hosts/usage.html",{"a_infos":a_infos,"uses":uses})
    except:
        return render(req, "4hosts/usage.html")


def hostssuggests(req):
    try:
        hoster = Hoster.objects.get(hos_id=int(req.session.get("user_id")))
        advices = Advice.objects.all().filter(hoster=hoster).filter(type_field=0)
        return render(req, "4hosts/suggests.html",{"advices":advices})
    except:
        return render(req, "4hosts/suggests.html")

def post_suggestion(req):
    try:
        data = req.POST.get("suggestion")

        hoster = Hoster.objects.all().filter(hos_id=req.session.get("user_id"))
        Advice.objects.create(hoster=hoster[0], content_field=data, state=1)
        return HttpResponse("操作成功")
    except:
        return HttpResponse("操作失败")


def post_go_repair(req):
    try:
        data = req.POST.get("go_repair")
        hoster = Hoster.objects.all().filter(hos_id=req.session.get("user_id"))
        Fix_Service.objects.create(hoster=hoster[0], content_field=data, state=1)
        # Advice.objects.create(hoster=hoster[0], content_field=data, state=0, type_re=1)  # 1 建议
        return HttpResponse("操作成功")
    except:
        return HttpResponse("操作失败")


def post_judge_repair(req):
    try:
        data = req.POST.get("judge_repair")
        work_id = req.GET.get("worker_id")
        serviceid = req.GET.get("serviceid")
        level = req.POST.get("level")
        print(level)
        worker = Worker.objects.get(w_id=work_id)
        hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
        service = Fix_Service.objects.get(fix_service_id=int(serviceid))
        # .filter(service_id_id=service).filter(work_id=worker)

        advice = Advice.objects.filter(hoster_id=hoster).filter(service_id_id=service).filter(workid_id=worker).filter(type_field=1)[0]

        advice.type_re = int(level)
        advice.content_field = data
        advice.state = 0
        advice.save()
        return HttpResponse("操作成功")
    except:
        return HttpResponse("操作失败")


def pays(req):
    try:
        hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
        bills = Bill.objects.all().filter(hoster_id=hoster)
        sumbill = 0
        for bill in bills:
            sumbill = sumbill + bill.b_amount

        return render(req, '4hosts/pays.html', {"bills": bills,"sumbill":sumbill})
    except :
        bill = None
        return render(req, '4hosts/pays.html', {"bills": bills})

def do_pay(req):
    try:
        hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
        bills = Bill.objects.all().filter(hoster_id=hoster)
        for bill in bills:
            bill.delete()
        return HttpResponse("缴费成功")
    except:
        return HttpResponse("缴费失败")

def park_rent_show(req):
    # 从数据库里取出数据
    parks = ParLot.objects.all().filter(avi=0)
    # 将数据发送到前段页面
    return render(req, '4hosts/park_rent.html', {"parks": parks})


def rentPark(req):
    try:
        park_id = req.GET.get("park_id")
        print(park_id)
        park = ParLot.objects.get(par_id=int(park_id))
        park.avi = 1
        hoster = Hoster.objects.get(hos_id=int(req.session.get("user_id")))
        park.host = hoster
        park.save()
        Bill.objects.create(b_name="租停车位",hoster_id=hoster,b_amount=park.rent)
        return HttpResponse("租赁成功")
    except:
        return HttpResponse("操作失败")



def park_buy_show(req):
    parks = ParLot.objects.all().filter(avi=0)
    # 将数据发送到前段页面
    return render(req, '4hosts/park_buy.html', {"parks": parks})


def buyPark(req):
    try:
        park_id = req.GET.get("park_id")
        park = ParLot.objects.get(par_id=int(park_id))
        park.avi = 2
        hoster = Hoster.objects.get(hos_id=int(req.session.get("user_id")))
        park.host = hoster
        park.save()
        Bill.objects.create(b_name="购买停车位", hoster_id=hoster, b_amount=park.price)
        return HttpResponse("购买成功")
    except:
        return HttpResponse("操作失败")


def house_rent_show(req):
    # 从数据库里取出数据
    houses = House.objects.all().filter(avi=0)
    # 将数据发送到前段页面
    return render(req, '4hosts/house_rent.html', {"houses": houses})


def rentHouse(req):
    try:
        house_id = req.GET.get("house_id")
        house = House.objects.get(ho_id=int(house_id))
        house.avi = 1
        hoster = Hoster.objects.get(hos_id=int(req.session.get("user_id")))
        house.host = hoster
        house.save()
        Bill.objects.create(b_name="租房", hoster_id=hoster, b_amount=house.rent)
        return HttpResponse("租赁成功")
    except:
        return HttpResponse("操作失败")

def house_buy_show(req):
    houses = House.objects.all().filter(avi=0)
    # 将数据发送到前段页面
    return render(req, '4hosts/house_buy.html', {"houses": houses})


def buyHouse(req):
    try:
        house_id = req.GET.get("house_id")
        house = House.objects.get(ho_id=int(house_id))
        house.avi = 2
        hoster = Hoster.objects.get(hos_id=int(req.session.get("user_id")))
        house.host = hoster
        house.save()
        Bill.objects.create(b_name="买房", hoster_id=hoster, b_amount=house.price)
        return HttpResponse("购买成功")
    except:
        return HttpResponse("操作失败")


def inout(req):
    host = Hoster.objects.get(hos_id=int(req.session.get("user_id")))
    print(host)
    inouts = InOut.objects.all().filter(hoster=host)
    return render(req, '4hosts/info_in_out.html', {"inouts": inouts})


def show_data(req):
    hoster = Hoster.objects.get(hos_id=int(req.session.get("user_id")))
    houses = House.objects.all().filter(host=hoster)
    parks = ParLot.objects.all().filter(host=hoster)
    return render(req, "4hosts/data.html", {"hoster": hoster, "houses": houses, "parks": parks})


def modify_data(req):
    try:
        hoster = Hoster.objects.get(hos_id=int(req.session.get("user_id")))
        sex = req.POST.get("sex")
        if sex == '男':
            hoster.sex = '1'
        else:
            hoster.sex = '0'
        contact = req.POST.get("contact")
        if contact != 'None':
            hoster.contact = int(contact)
        hoster.save()
        hoster = Hoster.objects.get(hos_id=req.session.get("user_id"))
        houses = House.objects.all().filter(host=hoster)
        parks = ParLot.objects.all().filter(host=hoster)
        return render(req, "4hosts/data.html", {"hoster": hoster, "houses": houses, "parks": parks})
    except:
        return HttpResponse("修改失败")




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
                    return redirect('Zone_manage:management_manager_index')
                elif type == 1:
                    return redirect('Zone_manage:business_administrator_index')
                elif type == 2:
                    return redirect('Zone_manage:hydropower_maintenance_worker_index')
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


            #张你的注册入口在这
            if type == 0:
                #管理处经理
                models.Worker.objects.create(name=username, sex=sex_num, type=type)
                #写入你想传过去的东西
                return redirect('Zone_manage:management_manager_index')
            elif type == 1:
                #业务管理员
                models.Worker.objects.create(name=username, sex=sex_num, type=type)

                return redirect('Zone_manage:business_administrator_index')
            elif type == 2:
                #水电维修工
                models.Worker.objects.create(name=username, sex=sex_num, type=type)

                return redirect('Zone_manage:hydropower_maintenance_worker_index')



            elif type == 3:
                models.Worker.objects.create(name=username,sex=sex_num,type = type)
                return HttpResponseRedirect('/security')
            elif type == 4:
                models.Hoster.objects.create(hos_name=username, sex=sex_num)
                hoster = models.Hoster.objects.get(hos_name=username)
                request.session["user_id"] = hoster.hos_id  # hosterid
                return render(request, '4.html',
                              {"userid": hoster.hos_id, "username": hoster.hos_name})  # hosterid hostername

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

        type = user.type
        name = user.username
        workers = models.Worker.objects.all().filter(type=type)

        work_s = None
        for work in workers:
            if work.name == name:
                work_s = work

        advice_s = models.Advice.objects.filter(workid=work_s.w_id)


        len = advice_s.count()

        hosts_boy = models.Hoster.objects.filter(sex='1')
        hosts_girl = models.Hoster.objects.filter(sex='0')

        boy_sum = hosts_boy.count()
        girl_sum = hosts_girl.count()
        sum = boy_sum+girl_sum
        return render(request, '3.html', {'user': user,'info':infos,'advice':advice_s,'len':len,'boy_num':boy_sum,'girl_num':girl_sum,'total':sum})


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

        worker = models.Worker.objects.filter(w_id=int(Wnumber))
        hoster = models.Hoster.objects.filter(hos_id=int(Hnumber))

        if worker.count()==0 or hoster.count()==0:
            error_message = 'workerid or hoster id not exists!'
            return render(request, 'form_validation.html', {'user': user,'error':error_message})
        else:
            succeed_message = 'Success!'
            models.InOut.objects.create(guest_name=Hname, worker=worker[0], contact=int(phone), remark=text, hoster=hoster[0])
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
def f_sa(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'fa_fo.html', {'user': user})

    if request.method == 'POST':
        user = request.user
        sa = request.POST['salary']
        se = request.POST['security']
        WD = request.POST['workid']

        worker = models.Worker.objects.filter(w_id=int(WD))


        if worker.count()==0:
            error_message = 'workerid id not exists!'
            return render(request, 'fa_fo.html', {'user': user,'error_sa':error_message})
        else:
            succeed_message = 'Success!'
            models.Salary.objects.create(base_sal=int(sa),up_sa=0,secu_sa=int(se),deduct=0,total=int(sa)+int(se),worker_id=int(WD))
            return render(request, 'fa_fo.html', {'user': user,'suc_sa':succeed_message})


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
        Expen = models.Expense.objects.all()
        Salary = models.Salary.objects.all()
        return render(request, 'fa_ta.html', {'user': user, 'BILLS': BILLS,'Expen': Expen,'Salary':Salary})


@login_required
def f_ca(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'fa_ca.html', {'user': user})
