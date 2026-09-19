from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path('guide/http-https/', views.transport_guide, name='transport-guide'),
    path('signup/', views.signup, name='signup'),
    path('account/', views.account, name='account'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'lab/sql-injection/vulnerable/',
        views.lab_vulnerable_login,
        name='lab-vulnerable-login',
    ),
    path(
        'lab/sql-injection/secure/',
        views.lab_secure_login,
        name='lab-secure-login',
    ),
    path('lab/sql-injection/result/', views.lab_result, name='lab-result'),
    path('lab/sql-injection/logout/', views.lab_logout, name='lab-logout'),
]
