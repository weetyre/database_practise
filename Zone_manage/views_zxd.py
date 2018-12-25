from django.shortcuts import render, redirect, HttpResponse
# from django.contrib.auth import authenticate, login, logout
# from .admin import UserCreationForm

# Create your views here.

from . import models


def homepage(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        return redirect('app_1:page')


# 维修服务
def business_administrator_fix_service(request):
    fix_services = models.Fix_Service.objects.all().order_by('-fix_service_id')
    workers = models.Worker.objects.all()
    return render(request, 'templates_zxd/Business_Administrator/fix_service.html',
                  {'fix_services': fix_services, 'workers': workers})


# 处理维修请求
def bussiness_fix_handle(request):
    fix_service_id = request.GET.get('id')
    operate_type = request.GET.get('operate_type')
    fix_worker = request.GET.get('fix_worker')
    user_name = request.user.username
    if operate_type == 'complete':
        fix = models.Fix_Service.objects.get(fix_service_id=fix_service_id)
        models.Fix_Service.objects.filter(fix_service_id=fix_service_id).update(state=0)
        worker = models.Worker.objects.get(name=user_name)
        models.Worker.objects.filter(name=user_name).update(avi=1)
        models.Worker.objects.filter(name=user_name).update(work_num=worker.work_num + 1)
        models.Advice.objects.create(hoster_id=fix.hoster_id, type_field=1, service_id_id=fix_service_id)
        return HttpResponse(1)
    elif operate_type == 'share':
        if models.Worker.objects.filter(w_id=fix_worker):
            if models.Worker.objects.get(w_id=fix_worker).avi == 1 or \
                    models.Worker.objects.get(w_id=fix_worker).avi is None:
                models.Fix_Service.objects.filter(fix_service_id=fix_service_id).update(workid_id=fix_worker)
                models.Worker.objects.filter(w_id=fix_worker).update(avi=0)
                return HttpResponse(2)
            else:
                return HttpResponse(500)
        else:
            return HttpResponse(404)
    else:
        return HttpResponse(404)


def business_administrator_index(request):
    rules = models.Rule.objects.all().order_by('-rule_id')
    infos = models.AInfo.objects.all().order_by('-id')
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
        models.House.objects.create(area=area, unit_n=unit, flour=ceng, bel_id=bel_id,price=price, rent=rent, avi=0)

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
        house_avi = request.POST.get('house_avi')
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
            if id == 'None' or id == '':
                models.House.objects.filter(ho_id=house_id).update(avi=0, host_id=None)
            elif models.Hoster.objects.filter(hos_id=id):
                models.House.objects.filter(ho_id=house_id).update(host_id=id, avi=house_avi)
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
    advices = models.Advice.objects.filter(type_field=0).order_by('-advice_id')
    all_ = []
    for advice in advices:
        work_name = models.Hoster.objects.get(hos_id=advice.hoster_id).hos_name
        all_.append(work_name)

    advices = zip(all_, advices)

    return render(request, 'templates_zxd/Business_Administrator/complaints.html', {'advices': advices})


def business_administrator_parking(request):
    if request.method == 'POST':
        park_avi = request.POST.get('park_avi')
        hoster = request.POST.get('hos_id')
        par_location = request.POST.get('par_location')
        gar_num = request.POST.get('gar_num')
        if hoster =="" or hoster == None:
            models.ParLot.objects.filter(gar_num=gar_num, par_location=par_location).update(avi=0, host=None)
        elif models.Hoster.objects.filter(hos_id=hoster):
            models.ParLot.objects.filter(gar_num=gar_num, par_location=par_location).update(avi=park_avi, host=hoster)
    par_lot = models.ParLot.objects.all()
    return render(request, 'templates_zxd/Business_Administrator/parking.html', {'parks': par_lot})


def bussiness_park_handle(request):
    gar_num = request.GET.get('gar_num')
    par_location = request.GET.get('par_location')
    price = request.GET.get('price')
    rent = request.GET.get('rent')
    hoster = request.GET.get('hoster')
    if request.GET.get('operate') == 'delete':
        # parks = models.ParLot.objects.all()
        parks = models.ParLot.objects.get(gar_num=gar_num, par_location=par_location).delete()
    elif request.GET.get('operate') == 'detail':
        park = models.ParLot.objects.get(gar_num=gar_num, par_location=par_location)
        return render(request, 'templates_zxd/Business_Administrator/detail_form_3.html', {'park_info': park})
    elif request.GET.get('operate') == 'add_post':
        if models.ParLot.objects.filter(gar_num=gar_num, par_location=par_location):
            return HttpResponse('404')
        else:
            models.ParLot.objects.create(gar_num=gar_num, par_location=par_location, price=price, rent=rent, avi=1)
    else:
        return HttpResponse(404)
    parks = models.ParLot.objects.all()
    return render(request, 'templates_zxd/Business_Administrator/table_park.html', {'parks': parks})


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

    rules = models.Rule.objects.all().order_by('-rule_id')
    infos = models.AInfo.objects.all().order_by('-id')
    print(rules)
    hoster_number = models.Hoster.objects.count()
    worker_number = models.Worker.objects.count()
    advice_count = models.Advice.objects.count()
    un_advice_count = models.Advice.objects.filter(state=0).count()
    return render(request, 'templates_zxd/Management_Manager/index.html',
                  {'rules': rules, 'hoster_number': hoster_number, 'worker_number': worker_number,
                   'infos': infos, 'advice_count': advice_count, 'un_advice_count': un_advice_count,
                   })


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
    rules = models.Rule.objects.all().order_by('-rule_id')
    infos = models.AInfo.objects.all().order_by('-id')
    hoster_number = models.Hoster.objects.count()
    equip_number = models.Equip.objects.count()
    advice_count = models.Advice.objects.filter(workid_id=3).count()
    un_advice_count = models.Advice.objects.filter(workid_id=3, state=0).count()
    return render(request, 'templates_zxd/Hydropower_Maintenance_Worker/index.html',
                  {'rules': rules, 'hoster_number': hoster_number, 'equip_number': equip_number,
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
                # e = models.Equip.objects.get(equ_id=equip_id)
                w = models.Worker.objects.get(w_id=worker_id)
                models.Fix.objects.create(workid=w, equ_id=equip_id)
            else:
                message1 = '输入不正确'
        if type == 'add':
            models.Equip.objects.create(loca=content)
    equips = models.Equip.objects.all()
    fixs = models.Fix.objects.all()
    return render(request, 'templates_zxd/Hydropower_Maintenance_Worker/mail.html',
                  {'equips': equips, 'message1': message1, 'fixs': fixs})


def hydropower_maintenance_worker_mail_checkin(request):
    message = ''
    if request.method == 'POST':
        hoster_id_id = request.POST.get('hosterid_id')
        b_name = request.POST.get('type')
        b_amount =eval(request.POST.get('amount'))
        user_name = request.user.username
        worker = models.Worker.objects.get(name=user_name)
        if models.Hoster.objects.filter(hos_id=hoster_id_id):
            models.Bill.objects.create(hoster_id_id=hoster_id_id, b_name=b_name, b_amount=b_amount, worker_id=worker.w_id)
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
    user_name = request.user.username
    worker = models.Worker.objects.get(name=user_name)
    advices = models.Advice.objects.filter(workid_id=worker.w_id).order_by('-advice_id')
    all_ = []
    for advice in advices:
        work_name = models.Hoster.objects.get(hos_id=advice.hoster_id).hos_name
        all_.append(work_name)

    advices = zip(all_, advices)

    fix_services = models.Fix_Service.objects.filter(workid_id=worker.w_id)
    comment = []
    for fix_service in fix_services:
        if models.Advice.objects.filter(service_id_id=fix_service.fix_service_id):
            comment.append(models.Advice.objects.get(service_id_id=fix_service.fix_service_id))
        else:
            comment.append(0)
    fix_services = zip(fix_services, comment)
    return render(request, 'templates_zxd/Hydropower_Maintenance_Worker/complaints.html',
                  {'advices': advices, 'fix_services': fix_services})


def hydropower_maintenance_baoxiao(request):
    message = ''
    if request.method == 'POST':
        duty_id = request.POST.get('duty_id')
        amount = request.POST.get('amount')
        name = request.POST.get('content')
        user_name = request.user.username
        worker = models.Worker.objects.get(name=user_name)
        if models.Expense.objects.filter(duty_id=duty_id):
            message = '税号重叠'
        else:
            models.Expense.objects.create(duty_id=duty_id, amount=amount, name=name,
                                          worker_id=worker.w_id)
            message = '添加成功'
    expense = models.Expense.objects.all()
    return render(request, 'templates_zxd/Hydropower_Maintenance_Worker/baoxiao.html', {'message': message, 'expense':expense})


