from django.db import models
from contratos.models import Contrato
from insumos.models import LancamentoInsumo


class Fatura(models.Model):
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('paga', 'Paga'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]

    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name='faturas', verbose_name='Contrato')
    mes_referencia = models.IntegerField('Mês de referência')
    ano_referencia = models.IntegerField('Ano de referência')
    data_vencimento = models.DateField('Data de vencimento')
    data_pagamento = models.DateField('Data de pagamento', null=True, blank=True)
    valor_aluguel = models.DecimalField('Valor do aluguel (R$)', max_digits=10, decimal_places=2)
    valor_insumos = models.DecimalField('Valor de insumos (R$)', max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField('Valor total (R$)', max_digits=10, decimal_places=2, default=0)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='aberta')
    observacoes = models.TextField('Observações', blank=True)
    lancamentos = models.ManyToManyField(LancamentoInsumo, blank=True, verbose_name='Lançamentos de insumos')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturas'
        ordering = ['-ano_referencia', '-mes_referencia']
        unique_together = ['contrato', 'mes_referencia', 'ano_referencia']

    def __str__(self):
        return f'Fatura {self.mes_referencia:02d}/{self.ano_referencia} - {self.contrato.cliente.nome}'

    def calcular_total(self):
        self.valor_insumos = sum(l.total for l in self.lancamentos.all())
        self.valor_total = self.valor_aluguel + self.valor_insumos
        self.save(update_fields=['valor_insumos', 'valor_total'])

    @property
    def mes_ano(self):
        import calendar
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        return f'{meses[self.mes_referencia - 1]}/{self.ano_referencia}'
