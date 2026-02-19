from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Contrato
from .forms import ContratoForm, ItemContratoFormSet
from .pdf import gerar_pdf_contrato


@login_required
def contrato_lista(request):
    status = request.GET.get('status', 'ativo')
    contratos = Contrato.objects.select_related('cliente', 'animal').filter(status=status)
    return render(request, 'contratos/lista.html', {'contratos': contratos, 'status': status})


@login_required
def contrato_detalhe(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    return render(request, 'contratos/detalhe.html', {'contrato': contrato})


@login_required
def contrato_novo(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        formset = ItemContratoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            contrato = form.save()
            formset.instance = contrato
            formset.save()
            contrato.recalcular_valor_mensal()
            messages.success(request, f'Contrato {contrato.numero} criado com sucesso!')
            return redirect('contrato_detalhe', pk=contrato.pk)
    else:
        form = ContratoForm()
        formset = ItemContratoFormSet()
        cliente_id = request.GET.get('cliente')
        if cliente_id:
            form.fields['cliente'].initial = cliente_id
    return render(request, 'contratos/form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Novo Contrato',
    })


@login_required
def contrato_editar(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        formset = ItemContratoFormSet(request.POST, instance=contrato)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            contrato.recalcular_valor_mensal()
            messages.success(request, 'Contrato atualizado com sucesso!')
            return redirect('contrato_detalhe', pk=contrato.pk)
    else:
        form = ContratoForm(instance=contrato)
        formset = ItemContratoFormSet(instance=contrato)
    return render(request, 'contratos/form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Editar Contrato',
        'contrato': contrato,
    })


@login_required
def contrato_pdf(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    buffer = gerar_pdf_contrato(contrato)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="contrato_{contrato.numero}.pdf"'
    return response


@login_required
def get_animais_cliente(request):
    from clientes.models import Animal
    from django.http import JsonResponse
    cliente_id = request.GET.get('cliente_id')
    animais = Animal.objects.filter(cliente_id=cliente_id, ativo=True).values('id', 'nome')
    return JsonResponse({'animais': list(animais)})
