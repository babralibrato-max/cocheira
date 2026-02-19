from django import forms
from .models import Fatura
from insumos.models import LancamentoInsumo


class FaturaForm(forms.ModelForm):
    class Meta:
        model = Fatura
        fields = ['contrato', 'mes_referencia', 'ano_referencia', 'data_vencimento', 'observacoes']
        widgets = {
            'contrato': forms.Select(attrs={'class': 'form-select'}),
            'mes_referencia': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '12'}),
            'ano_referencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
