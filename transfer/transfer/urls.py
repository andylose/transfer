"""transfer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from transferapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
    path('serve/', views.serve, name='serve'),
    path('transfer_form/', views.transfer_form, name='transfer_form'),
    path('check_transfer_form_progress/', views.check_transfer_form_progress, name='check_transfer_form_progress'),
    path('check_transfer_form_approval/', views.check_transfer_form_approval, name='check_transfer_form_approval'),
    path('final_check/', views.final_check, name='final_check'),
    path('student_serve/', views.student_serve, name='student_serve'),
    path('teacher_serve/', views.teacher_serve, name='teacher_serve'),
    path('school_admin_serve/', views.school_admin_serve, name='school_admin_serve'),
    path('already_filled/', views.already_filled, name='already_filled'),
    path('error_page/', views.error_page, name='error_page'),
    path('error_2/', views.error_2, name='error_2'),
]
