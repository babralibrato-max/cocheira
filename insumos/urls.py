from django.urls import path
from . import views

urlpatterns = [
    path('', views.lancamento_lista, name='lancamento_lista'),
    path('novo/', views.lancamento_novo, name='lancamento_novo'),
    path('<int:pk>/editar/', views.lancamento_editar, name='lancamento_editar'),
    path('<int:pk>/excluir/', views.lancamento_excluir, name='lancamento_excluir'),
    path('tipos/', views.tipo_insumo_lista, name='tipo_insumo_lista'),
    path('tipos/novo/', views.tipo_insumo_novo, name='tipo_insumo_novo'),
    path('ajax/preco/', views.get_preco_insumo, name='get_preco_insumo'),
]
