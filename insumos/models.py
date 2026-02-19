from django.db import models
from clientes.models import Cliente, Animal
from contratos.models import Contrato


class TipoInsumo(models.Model):
    nome = models.CharField('Nome', max_length=100)
    unidade = models.CharField('Unidade (kg, fardo, saco...)', max_length=20)
    preco_unitario = models.DecimalField('Preço unitário (R$)', max_digits=10, decimal_places=2)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Tipo de Insumo'
        verbose_name_plural = 'Tipos de Insumo'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.unidade})'


class LancamentoInsumo(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name='lancamentos', verbose_name='Contrato')
    tipo_insumo = models.ForeignKey(TipoInsumo, on_delete=models.PROTECT, verbose_name='Insumo')
    data = models.DateField('Data do fornecimento')
    quantidade = models.DecimalField('Quantidade', max_digits=10, decimal_places=3)
    preco_unitario = models.DecimalField('Preço unitário (R$)', max_digits=10, decimal_places=2)
    total = models.DecimalField('Total (R$)', max_digits=10, decimal_places=2, editable=False, default=0)
    observacao = models.CharField('Observação', max_length=200, blank=True)
    faturado = models.BooleanField('Faturado', default=False)

    class Meta:
        verbose_name = 'Lançamento de Insumo'
        verbose_name_plural = 'Lançamentos de Insumos'
        ordering = ['-data']

    def save(self, *args, **kwargs):
        self.total = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.data} - {self.tipo_insumo.nome} x{self.quantidade} ({self.contrato.cliente.nome})'
