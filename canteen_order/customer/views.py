from django.shortcuts import render
from .forms import LoginForm, RegisterForm, AdminForm 
from django.contrib import messages
from dish.models import Dish
from .models import Users

user_id = 0

def register(request):
    register_form = RegisterForm()
    if request.session.get('is_login', None):
        return render(request, 'index.html', locals())

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        print("[DEBUG][POST][STATE]:valid?{}", register_form.is_valid)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            try:
                user_cus = Users.objects.get(user_name=username)
                message = "您已注册，请登录"
                print("[DEBUG][POST][STATE]:您已注册，请登录！")
                return render(request, 'customer/login.html', locals())
            except:
                print("[DEBUG][POST][STATE]:u: {} p1{} p2{}", username, password1, password2)
                if password1 != password2:
                    print("[DEBUG][POST][STATE]:两次输入的密码不同！")
                    message = "两次密码应一致！"
                    return render(request, 'customer/register.html', locals())
                new_cus = Users.objects.create(user_name=username, user_psw=password1, user_balance=10000)
                new_cus.save()
                # 自动跳转到登录页面
                login_form = LoginForm()
                message = "注册成功！"
                return render(request, 'customer/login.html', locals())  # 自动跳转到登录页面
    else:
        print("[DEBUG][POST][STATE]:get!!!!!...")
        return render(request, 'customer/register.html', locals())
    return render(request, 'customer/register.html', locals())

def admin_login(request):
    admin_form = AdminForm()
    if request.method == "POST":
        admin_form = AdminForm(request.POST)
        if admin_form.is_valid():
            username = admin_form.cleaned_data['username']
            password = admin_form.cleaned_data['password']
            print("[DEBUG][POST][STATE]:u: {} p1{} p2{}", username, password, 1)
            try:
                print("[DEBUG][POST][STATE]:u: {} p1{} p2{}", username, password, 1)
                user_cus = Users.objects.get(user_name=username)
                print("[DEBUG][POST][STATE]:u: {} p1{} p2{}", username, password, user_cus.user_psw)
                if user_cus.user_psw == password and user_cus.user_status == 1:
                    messages.success(request, '{}登录成功！'.format(user_cus.user_name))
                    user_cus.save()
                    request.session['is_admin'] = True
                    request.session['is_login'] = True
                    user_id = user_cus.user_id
                    request.session['user_id'] = user_cus.user_id
                    request.session['user_name'] = user_cus.user_name
                    request.session['balance'] = user_cus.user_balance
                    context = {
                        'dish_list': Dish.objects.filter(store_id=user_cus.user_id)
                    }
                    combined_context = {**locals(), **context}
                    return render(request, 'admin_index.html', combined_context)
                else:
                    message = "密码不正确或您的账户已被冻结"
            except:
                message = "用户不存在，请注册"
    return render(request, 'customer/admin_login.html', locals())

def login(request):
    global user
    login_form = LoginForm()
    if request.session.get('is_login', None):
        return render(request, 'index.html', locals())
    
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            print("[DEBUG][POST][STATE]:u: {} p1{} p2{}", username, password, 1)
            try:
                print("[DEBUG][POST][STATE]:u: {} p1{} p2{}", username, password, 1)
                user_cus = Users.objects.get(user_name=username)
                print("[DEBUG][POST][STATE]:u: {} p1{} p2{}", username, password, user_cus.user_psw)
                if user_cus.user_psw == password and user_cus.user_status == 1:
                    messages.success(request, '{}登录成功！您的余额为{}'.format(user_cus.user_name, user_cus.user_balance))
                    user_cus.save()
                    request.session['is_admin'] = False
                    request.session['is_login'] = True
                    user_id = user_cus.user_id
                    request.session['user_id'] = user_cus.user_id
                    request.session['user_name'] = user_cus.user_name
                    request.session['balance'] = user_cus.user_balance
                    return render(request, 'index.html', locals())
                else:
                    message = "密码不正确或您的账户已被冻结"
            except:
                message = "用户不存在，请注册"
    return render(request, 'customer/login.html', locals())

def get_user_id():
    return user_id

def logout(request):
    request.session.flush()
    login_form = LoginForm()
    return render(request, 'customer/login.html', locals())

def index(request):
    return render(request, 'index.html', locals())