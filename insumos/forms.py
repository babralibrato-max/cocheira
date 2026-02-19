from django import forms
from .models import LancamentoInsumo, TipoInsumo


class LancamentoInsumoForm(forms.ModelForm):
    class Meta:
        model = LancamentoInsumo
        fields = ['contrato', 'tipo_insumo', 'data', 'quantidade', 'preco_unitario', 'observacao']
        widgets = {
            'contrato': forms.Select(attrs={'class': 'form-select'}),
            'tipo_insumo': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo_insumo'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'id': 'id_preco_unitario'}),
            'observacao': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TipoInsumoForm(forms.ModelForm):
    class Meta:
        model = TipoInsumo
        fields = ['nome', 'unidade', 'preco_unitario', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'unidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'kg, fardo, saco...'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
