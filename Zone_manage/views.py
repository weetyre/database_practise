from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from .admin import UserCreationForm
from .forms import LoginForm, ChangeEmailForm, MyPasswordChangeForm
from .models import MyUser


from .models import ParLot
from .models import House
from .models import InOut
from .models import Bill
from .models import Advice
from .models import Fix

def post_suggestion(req):
    data = req.POST.get("suggestion")
    print(data)
    # 增加一个数据，而不是修改
    advice = Advice.objects.all()[0]
    advice.hoster = req.session.get("user_id")
    advice.content_field = data
    advice.save()

    return render(req, '4hosts/suggests.html')


def post_go_repair(req):
    data = req.POST.get("go_repair")
    print(data)
    # 增加一个数据，而不是修改
    fix = Fix.objects.all()[0]
    fix.date_field = data
    fix.save()
    return render(req, '4hosts/go_repair.html')


def post_judge_repair(req):
    data = req.POST.get("judge_repair")
    print(data)
    # 此处向数据库插入信息
    return render(req, '4hosts/judge_repair.html')


def pays(req):
    bill = Bill.objects.get(req.session.get("user_id"))
    return render(req, '4hosts/pays.html', {"bill": bill})


def do_pay(req):
    bill = Bill.objects.get(req.session.get("user_id"))
    bill.b_amount = 0
    bill.save()

    bill = Bill.objects.get(req.session.get("user_id"))
    return render(req, '4hosts/pays.html', {"bill": bill})


def park_rent_show(req):
    # 从数据库里取出数据
    parks = ParLot.objects.all()
    # 将数据发送到前段页面
    return render(req, '4hosts/park_rent.html', {"parks": parks})


def rentPark(req):
    park_id = req.POST.get("park_id")
    pass

    return render(req, "4hosts/park_rent.html")

def park_buy_show(req):
    parks = ParLot.objects.all()
    # 将数据发送到前段页面
    return render(req, '4hosts/park_buy.html', {"parks": parks})


def buyPark(req):
    park_id = req.POST.get("park_id")
    pass

    return render(req, "4hosts/park_buy.html")


def house_rent_show(req):
    # 从数据库里取出数据
    houses = House.objects.all()
    # 将数据发送到前段页面
    return render(req, '4hosts/house_rent.html', {"houses": houses})


def rentHouse(req):
    house_id = req.POST.get("house_id")
    pass

    return render(req, "4hosts/house_rent.html")


def house_buy_show(req):
    houses = House.objects.all()
    # 将数据发送到前段页面
    return render(req, '4hosts/house_buy.html', {"houses": houses})


def buyHouse(req):
    hosue_id = req.POST.get("hosue_id")
    pass

    return render(req, "4hosts/house_buy.html")


def inout(req):
    inouts = InOut.objects.get(req.session.get("user_id"))
    return render(req, '4hosts/info_in_out.html', {"inouts": inouts})
















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
                    return render(request, '3.html', )
                elif type == 4:
                    return render(request, '4.html', )
                elif type == 5:
                    return render(request, '5.html', )
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
            type = request.POST['type']
            # password = make_password(form.cleaned_data['password'])
            MyUser.objects.create_user(username, email, sex, type, request.POST['password'])
            user = auth.authenticate(email=email, password=request.POST['password'])
            auth.login(request, user)
            if type == 0:
                return render(request, '0.html',)
            elif type == 1:
                return render(request, '1.html', )
            elif type == 2:
                return render(request, '2.html', )
            elif type == 3:
                return render(request, '3.html', )
            elif type == 4:
                return render(request, '4.html', )
            elif type == 5:
                return render(request, '5.html', )

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