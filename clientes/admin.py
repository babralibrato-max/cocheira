from django.contrib import admin
from .models import Cliente, Animal


class AnimalInline(admin.TabularInline):
    model = Animal
    extra = 0


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'telefone', 'cidade', 'ativo']
    list_filter = ['ativo', 'cidade']
    search_fields = ['nome', 'cpf']
    inlines = [AnimalInline]


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cliente', 'especie', 'raca', 'ativo']
    list_filter = ['especie', 'ativo']
    search_fields = ['nome', 'cliente__nome']
