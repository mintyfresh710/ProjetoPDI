from django.urls import path
from . import views

app_name = 'app_pdi'

urlpatterns = [
    path('', views.show_login, name='login'),
    path('cadastro/', views.show_cadastro, name='cadastro'),
    path('home/', views.show_home, name='home'),
    path('login/submit/', views.login_view, name='login_submit'),
    path('cadastro/submit/', views.cadastro_view, name='cadastro_submit'),
    path('plano-individual/', views.show_pi, name='plano_individual'),
    path('conta/', views.show_conta, name='conta'),
]
