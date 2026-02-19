"""
Script de configuração inicial da Cocheira.
Execute: python setup.py

Cria as tabelas, um superusuário padrão e os tipos de insumos comuns.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

print("=" * 50)
print("  SETUP - Sistema de Gestão de Cocheira")
print("=" * 50)

# 1. Migrations
print("\n[1/3] Criando banco de dados...")
call_command('migrate', verbosity=0)
print("  OK - Banco de dados criado.")

# 2. Superusuário
print("\n[2/3] Criando usuário administrador...")
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@cocheira.com', 'admin123')
    print("  OK - Usuário criado.")
    print("  Login: admin / Senha: admin123")
    print("  ATENÇÃO: Troque a senha após o primeiro acesso!")
else:
    print("  Usuário 'admin' já existe.")

# 3. Insumos padrão
print("\n[3/3] Cadastrando insumos padrão...")
from insumos.models import TipoInsumo

insumos_padrao = [
    ('Ração', 'kg', 3.50),
    ('Feno', 'fardo', 25.00),
    ('Serragem', 'saco', 15.00),
    ('Farelo de trigo', 'kg', 2.00),
    ('Milho grão', 'kg', 1.80),
    ('Sal mineral', 'kg', 4.50),
]

criados = 0
for nome, unidade, preco in insumos_padrao:
    obj, criado = TipoInsumo.objects.get_or_create(
        nome=nome,
        defaults={'unidade': unidade, 'preco_unitario': preco}
    )
    if criado:
        criados += 1

print(f"  OK - {criados} insumo(s) criado(s).")

print("\n" + "=" * 50)
print("  Setup concluído com sucesso!")
print("  Execute: python manage.py runserver")
print("  Acesse:  http://127.0.0.1:8000")
print("=" * 50 + "\n")
