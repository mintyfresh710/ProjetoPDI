from django.contrib import admin
from django.urls import path, include
from app_pdi import views as app_pdi_views
from pdi_form import views as pdi_form_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_pdi_views.show_login, name='login'),
    path('cadastro/', app_pdi_views.show_cadastro, name='cadastro'),
    path('home/', app_pdi_views.show_home, name='home'),
    path('login/submit/', app_pdi_views.login_view, name='login_submit'),
    path('cadastro/submit/', app_pdi_views.cadastro_view, name='cadastro_submit'),
    path('plano-individual/', app_pdi_views.plano_individual, name='plano_individual'),
    path('conta/', app_pdi_views.conta, name='conta'),
    path('formulario/', pdi_form_views.formulario, name='formulario'),
    path('salvar/', pdi_form_views.salvar_pdi, name='salvar_pdi'),
    path('visualizar/<int:pdi_id>/', pdi_form_views.visualizar_pdi, name='visualizar_pdi'),
    path('gerar-pdf/<int:pdi_id>/', pdi_form_views.gerar_pdf, name='gerar_pdf'),
]