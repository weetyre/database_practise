from django.shortcuts import render, redirect, HttpResponse
# from django.contrib.auth import authenticate, login, logout
# from .admin import UserCreationForm

# Create your views here.

from . import models
import json


def homepage(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        return redirect('app_1:page')


def business_administrator_index(request):
    rules = models.Rule.objects.all()
    infos = models.AInfo.objects.all()
    print(rules)
    hoster_number = models.Hoster.objects.count()
    house_number = models.House.objects.count()
    advice_count = models.Advice.objects.count()
    un_advice_count = models.Advice.objects.filter(state=0).count()
    return render(request, 'templates_zxd/Business_Administrator/index.html',
                  {'rules': rules, 'hoster_number': hoster_number, 'worker_number': house_number,
                   'infos': infos, 'advice_count': advice_count, 'un_advice_count': un_advice_count})


def business_administrator_mail(request):
    if request.method == 'POST':
        area = request.POST.get('hos_name')
        unit = request.POST.get('contact')
        ceng = request.POST.get('sex')
        bel_id = request.POST.get('bonus')
        price = request.POST.get('login_nam')
        rent = request.POST.get('pass')
        models.House.objects.create(area=area, unit_n=unit, flour=ceng, bel_id=bel_id,price=price, rent=rent)

    houses = models.House.objects.all()
    return render(request, 'templates_zxd/Business_Administrator/mail.html', {'hosters': houses})


# add
def business_administrator_checkin(request):
    error = ''
    if request.method == 'POST':
        print(request.POST)
        hos_name = request.POST.get('hos_name')
        contact = request.POST.get('contact')
        sex = request.POST.get('sex')
        login_nam = request.POST.get('login_nam')
        password = request.POST.get('pass')
        bonus = request.POST.get('bonus')
        id = request.POST.get('hos_id')
        house_id = request.POST.get('house_id')
        state = request.POST.get('avi')
        if request.POST.get('type') is None:
            print(request.POST)
            models.Hoster.objects.create(contact=contact, sex=sex, hos_name=hos_name,
                                         loign_nam=login_nam, pass_field=password, bonus=bonus,)
        elif request.POST.get('type') == 'form1_update':
            # MyUser.objects.create_user(username, email, sex, type, request.POST['password'])
            models.Hoster.objects.get(hos_id=id).delete()
            models.Hoster.objects.create(hos_id=id, contact=contact, sex=sex, hos_name=hos_name,
                                         loign_nam=login_nam, pass_field=password, bonus=bonus, )

            print('xxxxxxx')
        else:
            if models.Hoster.objects.filter(hos_id=id):
                models.House.objects.filter(ho_id=house_id).update(avi=state, host_id=id)
            else:
                error = '请先创建住户'
    hosters = models.Hoster.objects.all()
    houses = models.House.objects.all()
    return render(request, 'templates_zxd/Business_Administrator/checkin.html',
                  {'hosters': hosters, 'houses': houses, 'error': error})


def business_administrator_complaints(request):
    if request.method == 'POST':
        content_field = request.POST.get('post_content')
        title = request.POST.get('post_title')
        models.AInfo.objects.create(title=title, content=content_field)
    print(request)
    advices = models.Advice.objects.all().order_by('-advice_id')
    all_ = []
    for advice in advices:
        work_name = models.Hoster.objects.get(hos_id=advice.hoster_id).hos_name
        all_.append(work_name)

    advices = zip(all_, advices)

    return render(request, 'templates_zxd/Business_Administrator/complaints.html', {'advices': advices})


def business_administrator_parking(request):
    par_lot = models.ParLot.objects.all()
    return render(request, 'templates_zxd/Business_Administrator/parking.html', {'houses': par_lot})


def bussiness_checkin_delete(request):
    if request.method == 'GET':
        form = request.GET.get('content_type')
        print(form)
        if form == 'form1':
            hos_id = request.GET.get('id')
            models.Hoster.objects.filter(hos_id=hos_id).delete()
            return redirect('Zone_manage:business_administrator_checkin')
        else:
            house_id = request.GET.get('id')
            models.House.objects.filter(ho_id=house_id).delete()
            return redirect('Zone_manage:business_administrator_mail')
            return HttpResponse(2)

    return HttpResponse(404)


def bussiness_checkin_update(request):
    return HttpResponse(404)


def bussiness_checkin_detail(request):
    if request.method == 'GET':
        operate = request.GET.get('operate_type')
        if operate == 'detail':
            if request.GET.get('content_type') == 'form2':
                ho_id = request.GET.get('id')
                house = models.House.objects.get(ho_id=ho_id)
                # return HttpResponse(2)
                return render(request, 'templates_zxd/Business_Administrator/detail_form_2.html',
                              {'house': house})
            else:
                hos_id = request.GET.get('id')
                hoster_detail = models.Hoster.objects.get(hos_id=hos_id)
                # return HttpResponse(2)
                return render(request, 'templates_zxd/Business_Administrator/detail_form.html', {'hoster': hoster_detail})
        else:
            return HttpResponse(2)

    return HttpResponse(404)


def management_manager_advice_share(request):
    if request.method == 'GET':
        advice_id = request.GET.get('id')
        share_id = request.GET.get('share_id')
        if share_id:
            if models.Worker.objects.filter(w_id=share_id):
                models.Advice.objects.filter(advice_id=advice_id).update(workid_id=share_id)
                return HttpResponse(1)
            else:
                return HttpResponse(404)
    return HttpResponse(404)


################################
#                              #
#    Management_Manager View   #
#                              #
################################
def management_manager_index(request):
    rules = models.Rule.objects.all()
    infos = models.AInfo.objects.all()
    print(rules)
    hoster_number = models.Hoster.objects.count()
    worker_number = models.Worker.objects.count()
    advice_count = models.Advice.objects.count()
    un_advice_count = models.Advice.objects.filter(state=0).count()
    return render(request, 'templates_zxd/Management_Manager/index.html',
                  {'rules': rules, 'hoster_number': hoster_number, 'worker_number':worker_number,
                   'infos': infos, 'advice_count':advice_count, 'un_advice_count':un_advice_count})


def management_manager_mail(request):

    mails = models.Mail.objects.all()
    print(mails)
    return render(request, 'templates_zxd/Management_Manager/mail.html', {'mails': mails})


def management_manager_checkin(request):
    error = ''
    if request.method == 'POST':
        rule_id = request.POST.get('rule_id')
        content_field = request.POST.get('content_field')
        type_field = request.POST.get('type_field')
        if request.POST.get('type') == 'form1_update':
            print(rule_id, content_field)
            models.Rule.objects.filter(rule_id=rule_id).update(content_field=content_field, type_field=type_field)
        else:
            models.Rule.objects.create(content_field=content_field, type_field=type_field)
    rules = models.Rule.objects.all()

    return render(request, 'templates_zxd/Management_Manager/checkin.html', {'rules': rules})


def management_manager_complaints(request):
    if request.method == 'POST':
        content_field = request.POST.get('post_content')
        models.Advice.objects.create(content_field=content_field, workid_id=1, state=2)
    print(request)
    advices = models.Advice.objects.all().order_by('-advice_id')
    all_ = []
    for advice in advices:
        if advice.workid_id:
            work_name = models.Worker.objects.get(w_id=advice.workid_id).type
            all_.append(work_name)
        else:
            work_name = models.Hoster.objects.get(hos_id=advice.hoster_id).hos_name
            all_.append(9)

    advices = zip(all_, advices)

    return render(request, 'templates_zxd/Management_Manager/complaints.html', {'advices': advices})


def management_manager_parking(request):
    houses = models.InOut.objects.all()
    print(houses)
    return render(request, 'templates_zxd/Management_Manager/parking.html', {'houses': houses})


def management_manager_delete(request):
    if request.method == 'GET':
        form = request.GET.get('content_type')
        print(form)
        if form == 'form1':
            rule_id = request.GET.get('id')
            models.Rule.objects.get(rule_id=rule_id).delete()
            return redirect('Zone_manage:management_manager_checkin')
        else:
            return HttpResponse(2)

    return HttpResponse(404)


def management_manager_update(request):
    return HttpResponse(404)


def management_manager_detail(request):
    if request.method == 'GET':
        operate = request.GET.get('operate_type')
        if operate == 'detail':
            if request.GET.get('content_type') == 'form2':
                ho_id = request.GET.get('id')
                house = models.Rule.objects.get(ho_id=ho_id)
                # return HttpResponse(2)
                return render(request, 'templates_zxd/Business_Administrator/detail_form_2.html',
                              {'hoster': house})
            else:
                hos_id = request.GET.get('id')
                print(hos_id)
                hoster_detail = models.Rule.objects.get(rule_id=hos_id)
                # return HttpResponse(2)
                return render(request, 'templates_zxd/Management_Manager/detail_form.html', {'hoster': hoster_detail})
        else:
            return HttpResponse(2)

    return HttpResponse(404)


def management_manager_advice_finish(request):
    if request.method == 'GET':
        advice_id = request.GET.get('id')
        models.Advice.objects.filter(advice_id=advice_id).update(state=1)
    return HttpResponse(1)
################################
#                              #
#    Management_Manager View   #
#                              #
################################
def hydropower_maintenance_worker_index(request):
    rules = models.Rule.objects.all()
    infos = models.AInfo.objects.all()
    hoster_number = models.Equip.objects.count()
    worker_number = models.Worker.objects.count()
    advice_count = models.Advice.objects.filter(workid_id=3).count()
    un_advice_count = models.Advice.objects.filter(workid_id=3, state=0).count()
    return render(request, 'templates_zxd/Hydropower_Maintenance_Worker/index.html',
                  {'rules': rules, 'hoster_number': hoster_number, 'worker_number': worker_number,
                   'infos': infos, 'advice_count': advice_count, 'un_advice_count': un_advice_count})


def hydropower_maintenance_worker_mail(request):
    print(request.POST)
    equip_id = request.POST.get('form1_equip_id')
    worker_id = request.POST.get('form1_worker_id')
    type = request.POST.get('type')
    content = request.POST.get('form2_content')
    message1 = ''
    print(type,worker_id, equip_id)
    if request.method == 'POST':
        if type == 'fix':
            if models.Equip.objects.filter(equ_id=equip_id) and models.Worker.objects.filter(w_id=worker_id):
                e = models.Equip.objects.get(equ_id=equip_id)
                w = models.Worker.objects.get(w_id=worker_id)
                models.Fix.objects.create(workid=w, equ_id=equip_id)
            else:
                message1 = '输入不正确'
        if type == 'add':
            models.Equip.objects.create(loca=content)
    equips = models.Equip.objects.all()
    fixs = models.Fix.objects.all()
    return render(request, 'templates_zxd/Hydropower_Maintenance_Worker/mail.html',
                  {'equips': equips, 'message1': message1,'fixs':fixs})


def hydropower_maintenance_worker_mail_checkin(request):
    message = ''
    if request.method == 'POST':
        hoster_id_id = request.POST.get('hosterid_id')
        b_name = request.POST.get('type')
        b_amount =eval(request.POST.get('amount'))*2
        if models.Hoster.objects.filter(hos_id=hoster_id_id):
            models.Bill.objects.create(hoster_id_id=hoster_id_id, b_name=b_name, b_amount=b_amount, worker_id=3)
        else:
            message = 'fault'
    houses = models.Bill.objects.filter(b_name='维修费用').union(models.Bill.objects.filter(b_name='电费'))
    return render(request, 'templates_zxd/Hydropower_Maintenance_Worker/checkin.html', {'houses': houses, 'message': message})


def hydropower_maintenance_worker_complaints(request):
    if request.method == 'POST':
        content_field = request.POST.get('post_content')
        title = request.POST.get('post_title')
        models.AInfo.objects.create(title=title, content=content_field)
    print(request)
    advices = models.Advice.objects.filter(workid_id=3).order_by('-advice_id')
    all_ = []
    for advice in advices:
        work_name = models.Hoster.objects.get(hos_id=advice.hoster_id).hos_name
        all_.append(work_name)

    advices = zip(all_, advices)

    return render(request, 'templates_zxd/Hydropower_Maintenance_Worker/complaints.html',
                  {'advices': advices})


def hydropower_maintenance_baoxiao(request):
    message = ''

    if request.method == 'POST':
        duty_id = request.POST.get('duty_id')
        amount = request.POST.get('amount')
        if models.Expense.objects.filter(duty_id=duty_id):
            message = '税号重叠'
        else:
            models.Expense.objects.create(duty_id=duty_id, amount=amount, worker_id=3)
            message = '添加成功'
    expense = models.Expense.objects.all()
    return render(request, 'templates_zxd/Hydropower_Maintenance_Worker/baoxiao.html', {'message': message, 'expense':expense})


