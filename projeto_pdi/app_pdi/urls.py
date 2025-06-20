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
    path('conta/editar/', views.editar_perfil, name='editar_perfil'),
    path('conta/senha/', views.alterar_senha, name='alterar_senha'),

    path('api/w2h-plans/', views.w2h_plans_api, name='w2h_plans_api'),
    path('api/w2h-plans/<int:plan_id>/', views.w2h_plan_detail_api, name='w2h_plan_detail_api'),
]

