from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clientes/', views.cliente_lista, name='cliente_lista'),
    path('clientes/novo/', views.cliente_novo, name='cliente_novo'),
    path('clientes/<int:pk>/', views.cliente_detalhe, name='cliente_detalhe'),
    path('clientes/<int:pk>/editar/', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:cliente_pk>/animal/novo/', views.animal_novo, name='animal_novo'),
    path('animais/<int:pk>/editar/', views.animal_editar, name='animal_editar'),
]
