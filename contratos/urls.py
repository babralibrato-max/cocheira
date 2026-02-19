from django.urls import path
from . import views

urlpatterns = [
    path('', views.contrato_lista, name='contrato_lista'),
    path('novo/', views.contrato_novo, name='contrato_novo'),
    path('<int:pk>/', views.contrato_detalhe, name='contrato_detalhe'),
    path('<int:pk>/editar/', views.contrato_editar, name='contrato_editar'),
    path('<int:pk>/pdf/', views.contrato_pdf, name='contrato_pdf'),
    path('ajax/animais/', views.get_animais_cliente, name='get_animais_cliente'),
]
