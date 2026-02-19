from django.urls import path
from . import views

urlpatterns = [
    path('', views.fatura_lista, name='fatura_lista'),
    path('nova/', views.fatura_nova, name='fatura_nova'),
    path('gerar-mensal/', views.fatura_gerar_mensal, name='fatura_gerar_mensal'),
    path('<int:pk>/', views.fatura_detalhe, name='fatura_detalhe'),
    path('<int:pk>/pagar/', views.fatura_marcar_paga, name='fatura_marcar_paga'),
    path('relatorio/', views.relatorio_mensal, name='relatorio_mensal'),
]
