from django.contrib import admin
from .models import TipoInsumo, LancamentoInsumo


@admin.register(TipoInsumo)
class TipoInsumoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'unidade', 'preco_unitario', 'ativo']


@admin.register(LancamentoInsumo)
class LancamentoInsumoAdmin(admin.ModelAdmin):
    list_display = ['data', 'contrato', 'tipo_insumo', 'quantidade', 'total', 'faturado']
    list_filter = ['faturado', 'tipo_insumo']
    date_hierarchy = 'data'
