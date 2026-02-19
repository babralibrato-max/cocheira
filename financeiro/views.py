from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
import datetime
from .models import Fatura
from .forms import FaturaForm
from contratos.models import Contrato
from insumos.models import LancamentoInsumo


@login_required
def fatura_lista(request):
    status = request.GET.get('status', '')
    mes = request.GET.get('mes', '')
    ano = request.GET.get('ano', str(datetime.date.today().year))

    faturas = Fatura.objects.select_related('contrato__cliente', 'contrato__animal')

    if status:
        faturas = faturas.filter(status=status)
    if mes:
        faturas = faturas.filter(mes_referencia=mes)
    if ano:
        faturas = faturas.filter(ano_referencia=ano)

    total_aberto = faturas.filter(status='aberta').aggregate(t=Sum('valor_total'))['t'] or 0
    total_pago = faturas.filter(status='paga').aggregate(t=Sum('valor_total'))['t'] or 0

    context = {
        'faturas': faturas.order_by('-ano_referencia', '-mes_referencia'),
        'status': status,
        'mes': mes,
        'ano': ano,
        'total_aberto': total_aberto,
        'total_pago': total_pago,
        'meses': range(1, 13),
        'anos': range(datetime.date.today().year - 2, datetime.date.today().year + 2),
    }
    return render(request, 'financeiro/lista.html', context)


@login_required
def fatura_detalhe(request, pk):
    fatura = get_object_or_404(Fatura, pk=pk)
    return render(request, 'financeiro/detalhe.html', {'fatura': fatura})


@login_required
def fatura_nova(request):
    if request.method == 'POST':
        form = FaturaForm(request.POST)
        if form.is_valid():
            fatura = form.save(commit=False)
            fatura.valor_aluguel = fatura.contrato.valor_mensal
            fatura.save()
            form.save_m2m()
            fatura.calcular_total()
            messages.success(request, f'Fatura gerada: {fatura}')
            return redirect('fatura_detalhe', pk=fatura.pk)
    else:
        form = FaturaForm()
        contrato_id = request.GET.get('contrato')
        if contrato_id:
            form.fields['contrato'].initial = contrato_id
    return render(request, 'financeiro/form.html', {'form': form, 'titulo': 'Nova Fatura'})


@login_required
def fatura_gerar_mensal(request):
    """Gera faturas para todos os contratos ativos do mês/ano informado."""
    if request.method == 'POST':
        mes = int(request.POST.get('mes'))
        ano = int(request.POST.get('ano'))
        contratos = Contrato.objects.filter(status='ativo')
        geradas = 0
        existentes = 0

        for contrato in contratos:
            import calendar
            dia_vcto = min(contrato.dia_vencimento, calendar.monthrange(ano, mes)[1])
            fatura, criada = Fatura.objects.get_or_create(
                contrato=contrato,
                mes_referencia=mes,
                ano_referencia=ano,
                defaults={
                    'data_vencimento': datetime.date(ano, mes, dia_vcto),
                    'valor_aluguel': contrato.valor_mensal,
                    'valor_total': contrato.valor_mensal,
                }
            )
            if criada:
                # Vincular lançamentos de insumos não faturados do período
                lancamentos = LancamentoInsumo.objects.filter(
                    contrato=contrato,
                    data__month=mes,
                    data__year=ano,
                    faturado=False
                )
                fatura.lancamentos.set(lancamentos)
                lancamentos.update(faturado=True)
                fatura.calcular_total()
                geradas += 1
            else:
                existentes += 1

        messages.success(request, f'{geradas} fatura(s) gerada(s). {existentes} já existia(m).')
        return redirect('fatura_lista')

    hoje = datetime.date.today()
    return render(request, 'financeiro/gerar_mensal.html', {
        'mes': hoje.month,
        'ano': hoje.year,
        'meses': range(1, 13),
        'anos': range(hoje.year - 1, hoje.year + 2),
    })


@login_required
def fatura_marcar_paga(request, pk):
    fatura = get_object_or_404(Fatura, pk=pk)
    if request.method == 'POST':
        data_pgto = request.POST.get('data_pagamento') or datetime.date.today()
        fatura.data_pagamento = data_pgto
        fatura.status = 'paga'
        fatura.save()
        messages.success(request, 'Fatura marcada como paga!')
    return redirect('fatura_detalhe', pk=pk)


@login_required
def relatorio_mensal(request):
    mes = int(request.GET.get('mes', datetime.date.today().month))
    ano = int(request.GET.get('ano', datetime.date.today().year))

    faturas = Fatura.objects.filter(
        mes_referencia=mes, ano_referencia=ano
    ).select_related('contrato__cliente').order_by('contrato__cliente__nome')

    totais = faturas.aggregate(
        total_aluguel=Sum('valor_aluguel'),
        total_insumos=Sum('valor_insumos'),
        total_geral=Sum('valor_total'),
    )

    context = {
        'faturas': faturas,
        'totais': totais,
        'mes': mes,
        'ano': ano,
        'meses': range(1, 13),
        'anos': range(datetime.date.today().year - 2, datetime.date.today().year + 2),
    }
    return render(request, 'financeiro/relatorio.html', context)
