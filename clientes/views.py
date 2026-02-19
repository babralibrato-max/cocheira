from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente, Animal
from .forms import ClienteForm, AnimalForm


@login_required
def dashboard(request):
    from contratos.models import Contrato
    from financeiro.models import Fatura
    from django.db.models import Sum
    import datetime

    hoje = datetime.date.today()
    clientes_ativos = Cliente.objects.filter(ativo=True).count()
    contratos_ativos = Contrato.objects.filter(status='ativo').count()
    faturas_abertas = Fatura.objects.filter(status='aberta').count()
    faturas_vencidas = Fatura.objects.filter(status='aberta', data_vencimento__lt=hoje).count()
    receita_mes = Fatura.objects.filter(
        status='paga',
        data_pagamento__month=hoje.month,
        data_pagamento__year=hoje.year
    ).aggregate(total=Sum('valor_total'))['total'] or 0

    ultimas_faturas = Fatura.objects.select_related('contrato__cliente').order_by('-data_criacao')[:5]

    context = {
        'clientes_ativos': clientes_ativos,
        'contratos_ativos': contratos_ativos,
        'faturas_abertas': faturas_abertas,
        'faturas_vencidas': faturas_vencidas,
        'receita_mes': receita_mes,
        'ultimas_faturas': ultimas_faturas,
    }
    return render(request, 'dashboard.html', context)


@login_required
def cliente_lista(request):
    query = request.GET.get('q', '')
    clientes = Cliente.objects.filter(ativo=True)
    if query:
        clientes = clientes.filter(nome__icontains=query)
    return render(request, 'clientes/lista.html', {'clientes': clientes, 'query': query})


@login_required
def cliente_detalhe(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'clientes/detalhe.html', {'cliente': cliente})


@login_required
def cliente_novo(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente.nome} cadastrado com sucesso!')
            return redirect('cliente_detalhe', pk=cliente.pk)
    else:
        form = ClienteForm()
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Novo Cliente'})


@login_required
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('cliente_detalhe', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Editar Cliente', 'cliente': cliente})


@login_required
def animal_novo(request, cliente_pk):
    cliente = get_object_or_404(Cliente, pk=cliente_pk)
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.cliente = cliente
            animal.save()
            messages.success(request, f'Animal {animal.nome} cadastrado com sucesso!')
            return redirect('cliente_detalhe', pk=cliente.pk)
    else:
        form = AnimalForm()
    return render(request, 'clientes/animal_form.html', {'form': form, 'cliente': cliente})


@login_required
def animal_editar(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal atualizado com sucesso!')
            return redirect('cliente_detalhe', pk=animal.cliente.pk)
    else:
        form = AnimalForm(instance=animal)
    return render(request, 'clientes/animal_form.html', {'form': form, 'animal': animal, 'cliente': animal.cliente})
