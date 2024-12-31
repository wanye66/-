# accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

# 视图函数，直接重定向到 home
def redirect_to_home(request):
    return redirect('home')  # 这里使用 URL 名称 'home' 进行重定向

urlpatterns = [
    path('', redirect_to_home, name='accounts_redirect'),  # 访问 /accounts/ 会重定向到 home
    path('home/', views.home, name='home'),  # 主页
    path('login/', views.login_view, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # 登出功能
    path('delayed_redirect/', views.delayed_redirect, name='delayed_redirect'),
    path('register/', views.register_view, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    # 其他URL配置
]
