from django.db import models
from clientes.models import Cliente, Animal
from decimal import Decimal


class Contrato(models.Model):
    TIPO_CHOICES = [
        ('baia', 'Baia'),
        ('pasto', 'Pasto'),
        ('baia_pasto', 'Baia + Pasto'),
        ('outro', 'Outro'),
    ]
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('encerrado', 'Encerrado'),
        ('suspenso', 'Suspenso'),
    ]

    numero = models.CharField('Nº do Contrato', max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='contratos', verbose_name='Cliente')
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, related_name='contratos', verbose_name='Animal')
    tipo = models.CharField('Tipo de aluguel', max_length=20, choices=TIPO_CHOICES)
    identificacao_local = models.CharField('Identificação (ex: Baia 3, Pasto A)', max_length=100, blank=True)
    data_inicio = models.DateField('Data de início')
    data_fim = models.DateField('Data de término', null=True, blank=True)
    valor_mensal = models.DecimalField('Valor mensal (R$)', max_digits=10, decimal_places=2, default=0)
    dia_vencimento = models.IntegerField('Dia de vencimento', default=10)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='ativo')
    clausulas_extras = models.TextField('Cláusulas adicionais', blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-data_inicio']

    def __str__(self):
        return f'Contrato {self.numero} - {self.cliente.nome} / {self.animal.nome}'

    def recalcular_valor_mensal(self):
        """Soma todos os itens e atualiza o valor_mensal."""
        total = sum(item.subtotal for item in self.itens.all())
        self.valor_mensal = total
        self.save(update_fields=['valor_mensal'])
        return total

    def save(self, *args, **kwargs):
        if not self.numero:
            import datetime
            ano = datetime.date.today().year
            ultimo = Contrato.objects.filter(numero__startswith=str(ano)).count()
            self.numero = f'{ano}-{str(ultimo + 1).zfill(3)}'
        super().save(*args, **kwargs)


class ItemContrato(models.Model):
    CATEGORIA_CHOICES = [
        ('aluguel', 'Aluguel'),
        ('racao', 'Ração'),
        ('feno', 'Feno'),
        ('serragem', 'Serragem'),
        ('servico', 'Serviço / Mão de obra'),
        ('outro', 'Outro'),
    ]

    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='itens', verbose_name='Contrato')
    categoria = models.CharField('Categoria', max_length=20, choices=CATEGORIA_CHOICES)
    descricao = models.CharField('Descrição', max_length=200)
    quantidade = models.DecimalField('Quantidade', max_digits=10, decimal_places=3, default=1)
    unidade = models.CharField('Unidade', max_length=30, blank=True, default='mês')
    valor_unitario = models.DecimalField('Valor unitário (R$)', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField('Subtotal (R$)', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Item do Contrato'
        verbose_name_plural = 'Itens do Contrato'
        ordering = ['categoria']

    def save(self, *args, **kwargs):
        self.subtotal = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_categoria_display()} - {self.descricao}'
