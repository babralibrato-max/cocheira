from django.contrib import admin
from .models import Contrato


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'animal', 'tipo', 'valor_mensal', 'status', 'data_inicio']
    list_filter = ['status', 'tipo']
    search_fields = ['numero', 'cliente__nome', 'animal__nome']
    date_hierarchy = 'data_inicio'
