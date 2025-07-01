from django.urls import path
from . import views

app_name = 'pdi_form'

urlpatterns = [
    path('formulario/', views.formulario, name='formulario'),
    path('salvar/', views.salvar_pdi, name='salvar_pdi'),   
    path('visualizar/<int:pdi_id>/', views.visualizar_pdi, name='visualizar_pdi'),
    path('gerar-pdf/<int:pdi_id>/', views.gerar_pdf, name='gerar_pdf'),
]
