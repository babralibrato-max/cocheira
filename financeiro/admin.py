from django.contrib import admin
from .models import Fatura


@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'contrato', 'valor_total', 'status', 'data_vencimento']
    list_filter = ['status', 'ano_referencia', 'mes_referencia']
    search_fields = ['contrato__cliente__nome', 'contrato__numero']
