from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# 主页面视图
def home(request):
    return render(request, 'accounts/home.html')

def redirect_to_home(request):
    return redirect('home')

# 登录视图
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('delayed_redirect')  # 登录成功后跳转到延迟页面
        else:
            messages.error(request, '用户名或密码错误')

    return render(request, 'accounts/login.html')

# 延迟页面视图
def delayed_redirect(request):
    return render(request, 'accounts/delayed_redirect.html')

# 忘记密码视图
def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_reset_email(email)
            messages.success(request, "重置密码的链接已发送到您的邮箱。")
            return redirect('forgot_password')  # 重定向到相同页面，显示成功消息
    else:
        form = PasswordResetForm()

    return render(request, 'accounts/forgot_password.html', {'form': form})

# 发送重置密码邮件
def send_reset_email(email):
    reset_link = f"{settings.SITE_URL}/reset_password/{email}"  # 可根据需求修改链接格式
    subject = "密码重置请求"
    message = f"点击此链接重置您的密码: {reset_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

# 注册视图
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # 验证密码是否一致
        if password != confirm_password:
            messages.error(request, '密码和确认密码不一致')
            return render(request, 'accounts/register.html')  # 返回注册页面并显示错误信息

        # 检查用户名和邮箱是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在，请选择其他用户名')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, '邮箱已被注册，请使用其他邮箱')
            return render(request, 'accounts/register.html')

        # 创建新用户并保存
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # 注册成功，提示信息并跳转到登录页面
        messages.success(request, '注册成功！请登录')
        return redirect('login')  # 注册成功后重定向到登录页面

    return render(request, 'accounts/register.html')
