from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from .models import TipoInsumo, LancamentoInsumo
from .forms import LancamentoInsumoForm, TipoInsumoForm


@login_required
def lancamento_lista(request):
    from contratos.models import Contrato
    mes = int(request.GET.get('mes', datetime.date.today().month))
    ano = int(request.GET.get('ano', datetime.date.today().year))
    contrato_id = request.GET.get('contrato', '')

    lancamentos = LancamentoInsumo.objects.select_related(
        'contrato__cliente', 'tipo_insumo'
    ).filter(data__month=mes, data__year=ano)

    if contrato_id:
        lancamentos = lancamentos.filter(contrato_id=contrato_id)

    contratos = Contrato.objects.filter(status='ativo').select_related('cliente', 'animal')

    context = {
        'lancamentos': lancamentos,
        'mes': mes,
        'ano': ano,
        'contratos': contratos,
        'contrato_id': contrato_id,
        'meses': range(1, 13),
        'anos': range(datetime.date.today().year - 2, datetime.date.today().year + 2),
    }
    return render(request, 'insumos/lista.html', context)


@login_required
def lancamento_novo(request):
    if request.method == 'POST':
        form = LancamentoInsumoForm(request.POST)
        if form.is_valid():
            lancamento = form.save()
            messages.success(request, 'Lançamento registrado com sucesso!')
            return redirect('lancamento_lista')
    else:
        form = LancamentoInsumoForm()
        contrato_id = request.GET.get('contrato')
        if contrato_id:
            form.fields['contrato'].initial = contrato_id
    return render(request, 'insumos/form.html', {'form': form, 'titulo': 'Novo Lançamento'})


@login_required
def lancamento_editar(request, pk):
    lancamento = get_object_or_404(LancamentoInsumo, pk=pk)
    if request.method == 'POST':
        form = LancamentoInsumoForm(request.POST, instance=lancamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lançamento atualizado!')
            return redirect('lancamento_lista')
    else:
        form = LancamentoInsumoForm(instance=lancamento)
    return render(request, 'insumos/form.html', {'form': form, 'titulo': 'Editar Lançamento'})


@login_required
def lancamento_excluir(request, pk):
    lancamento = get_object_or_404(LancamentoInsumo, pk=pk)
    if not lancamento.faturado:
        lancamento.delete()
        messages.success(request, 'Lançamento excluído.')
    else:
        messages.error(request, 'Não é possível excluir um lançamento já faturado.')
    return redirect('lancamento_lista')


@login_required
def tipo_insumo_lista(request):
    tipos = TipoInsumo.objects.filter(ativo=True)
    return render(request, 'insumos/tipos.html', {'tipos': tipos})


@login_required
def tipo_insumo_novo(request):
    if request.method == 'POST':
        form = TipoInsumoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de insumo cadastrado!')
            return redirect('tipo_insumo_lista')
    else:
        form = TipoInsumoForm()
    return render(request, 'insumos/tipo_form.html', {'form': form})


@login_required
def get_preco_insumo(request):
    from django.http import JsonResponse
    tipo_id = request.GET.get('tipo_id')
    try:
        tipo = TipoInsumo.objects.get(pk=tipo_id)
        return JsonResponse({'preco': str(tipo.preco_unitario)})
    except TipoInsumo.DoesNotExist:
        return JsonResponse({'preco': '0'})
