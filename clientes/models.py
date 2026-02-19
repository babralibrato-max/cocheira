from django.db import models


class Cliente(models.Model):
    nome = models.CharField('Nome completo', max_length=200)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    rg = models.CharField('RG', max_length=20, blank=True)
    telefone = models.CharField('Telefone', max_length=20)
    email = models.EmailField('E-mail', blank=True)
    endereco = models.CharField('Endereço', max_length=300, blank=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True)
    estado = models.CharField('Estado', max_length=2, blank=True)
    cep = models.CharField('CEP', max_length=9, blank=True)
    data_cadastro = models.DateField('Data de cadastro', auto_now_add=True)
    ativo = models.BooleanField('Ativo', default=True)
    observacoes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Animal(models.Model):
    ESPECIE_CHOICES = [
        ('cavalo', 'Cavalo'),
        ('egua', 'Égua'),
        ('potro', 'Potro'),
        ('burro', 'Burro'),
        ('mula', 'Mula'),
        ('outro', 'Outro'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='animais', verbose_name='Proprietário')
    nome = models.CharField('Nome do animal', max_length=100)
    especie = models.CharField('Espécie', max_length=20, choices=ESPECIE_CHOICES, default='cavalo')
    raca = models.CharField('Raça', max_length=100, blank=True)
    cor = models.CharField('Cor/Pelagem', max_length=100, blank=True)
    data_nascimento = models.DateField('Data de nascimento', null=True, blank=True)
    registro = models.CharField('Nº de Registro', max_length=100, blank=True)
    observacoes = models.TextField('Observações', blank=True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animais'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.cliente.nome})'
