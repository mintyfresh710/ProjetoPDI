from django.contrib import admin
from django.urls import path
from app_pdi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_login, name='login'),
    path('cadastro/', views.show_cadastro, name='cadastro'),
    path('home/', views.show_home, name='home'),
    path('login/submit/', views.login_view, name='login_submit'),
    path('cadastro/submit/', views.cadastro_view, name='cadastro_submit'),
]
