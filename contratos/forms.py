from django import forms
from django.forms import inlineformset_factory
from .models import Contrato, ItemContrato


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['cliente', 'animal', 'tipo', 'identificacao_local',
                  'data_inicio', 'data_fim', 'dia_vencimento',
                  'status', 'clausulas_extras']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select', 'id': 'id_cliente'}),
            'animal': forms.Select(attrs={'class': 'form-select', 'id': 'id_animal'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'identificacao_local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Baia 3, Pasto A'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dia_vencimento': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '31'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'clausulas_extras': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ItemContratoForm(forms.ModelForm):
    class Meta:
        model = ItemContrato
        fields = ['categoria', 'descricao', 'quantidade', 'unidade', 'valor_unitario']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Ex: Ração 5kg/dia'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.001'}),
            'unidade': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'mês, kg, fardo...'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control form-control-sm item-valor', 'step': '0.01'}),
        }


ItemContratoFormSet = inlineformset_factory(
    Contrato,
    ItemContrato,
    form=ItemContratoForm,
    extra=1,
    can_delete=True,
)
