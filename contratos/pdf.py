from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import datetime


def gerar_pdf_contrato(contrato):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.5*cm,
        leftMargin=2.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()

    style_titulo = ParagraphStyle(
        'Titulo',
        parent=styles['Heading1'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=6,
        textColor=colors.HexColor('#2c3e50'),
    )
    style_subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=colors.HexColor('#7f8c8d'),
    )
    style_secao = ParagraphStyle(
        'Secao',
        parent=styles['Heading2'],
        fontSize=11,
        spaceAfter=4,
        spaceBefore=12,
        textColor=colors.HexColor('#2c3e50'),
    )
    style_body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=16,
    )
    style_assinatura = ParagraphStyle(
        'Assinatura',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
    )

    story = []

    # Cabeçalho
    story.append(Paragraph('CONTRATO DE PRESTAÇÃO DE SERVIÇOS', style_titulo))
    story.append(Paragraph(f'Cocheira - Contrato Nº {contrato.numero}', style_subtitulo))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#2c3e50')))
    story.append(Spacer(1, 0.4*cm))

    # Dados do contrato em tabela
    story.append(Paragraph('DADOS DO CONTRATO', style_secao))

    tipo_display = dict(contrato.TIPO_CHOICES).get(contrato.tipo, contrato.tipo)
    dados_contrato = [
        ['Nº do Contrato:', contrato.numero, 'Tipo:', tipo_display],
        ['Data de Início:', contrato.data_inicio.strftime('%d/%m/%Y'),
         'Data de Término:', contrato.data_fim.strftime('%d/%m/%Y') if contrato.data_fim else 'Indeterminado'],
        ['Local:', contrato.identificacao_local or '-',
         'Valor Mensal:', f'R$ {contrato.valor_mensal:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')],
        ['Vencimento:', f'Dia {contrato.dia_vencimento}', '', ''],
    ]

    table_contrato = Table(dados_contrato, colWidths=[3.5*cm, 5*cm, 3.5*cm, 5*cm])
    table_contrato.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#f8f9fa'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(table_contrato)

    # Dados do cliente
    story.append(Paragraph('DADOS DO CONTRATANTE', style_secao))
    cliente = contrato.cliente

    dados_cliente = [
        ['Nome:', cliente.nome, 'CPF:', cliente.cpf],
        ['RG:', cliente.rg or '-', 'Telefone:', cliente.telefone],
        ['E-mail:', cliente.email or '-', 'CEP:', cliente.cep or '-'],
        ['Endereço:', f'{cliente.endereco}, {cliente.cidade}/{cliente.estado}' if cliente.endereco else '-', '', ''],
    ]

    table_cliente = Table(dados_cliente, colWidths=[2.5*cm, 6*cm, 2.5*cm, 6*cm])
    table_cliente.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#f8f9fa'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('SPAN', (1, 3), (3, 3)),
    ]))
    story.append(table_cliente)

    # Dados do animal
    story.append(Paragraph('DADOS DO ANIMAL', style_secao))
    animal = contrato.animal

    dados_animal = [
        ['Nome:', animal.nome, 'Espécie:', animal.get_especie_display()],
        ['Raça:', animal.raca or '-', 'Cor/Pelagem:', animal.cor or '-'],
        ['Registro:', animal.registro or '-', 'Nascimento:', animal.data_nascimento.strftime('%d/%m/%Y') if animal.data_nascimento else '-'],
    ]

    table_animal = Table(dados_animal, colWidths=[2.5*cm, 6*cm, 2.5*cm, 6*cm])
    table_animal.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#f8f9fa'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(table_animal)

    # Composição do valor mensal
    itens = list(contrato.itens.all())
    if itens:
        story.append(Paragraph('COMPOSIÇÃO DO VALOR MENSAL', style_secao))
        header_itens = [['Categoria', 'Descrição', 'Qtd', 'Unidade', 'Valor Unit.', 'Subtotal']]
        linhas_itens = header_itens + [
            [
                item.get_categoria_display(),
                item.descricao,
                str(item.quantidade).rstrip('0').rstrip('.'),
                item.unidade,
                f'R$ {item.valor_unitario:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
                f'R$ {item.subtotal:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
            ]
            for item in itens
        ]
        linhas_itens.append([
            '', '', '', '', 'TOTAL MENSAL:',
            f'R$ {contrato.valor_mensal:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
        ])

        table_itens = Table(linhas_itens, colWidths=[3*cm, 5.5*cm, 1.5*cm, 1.8*cm, 2.5*cm, 2.7*cm])
        table_itens.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (4, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.HexColor('#f8f9fa'), colors.white]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d4edda')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (4, 0), (-1, -1), 'RIGHT'),
        ]))
        story.append(table_itens)

    # Cláusulas
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('CLÁUSULAS E CONDIÇÕES', style_secao))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#dee2e6')))
    story.append(Spacer(1, 0.2*cm))

    clausulas = [
        ('1ª', 'DO OBJETO', f'O presente contrato tem por objeto a locação de {tipo_display.lower()} '
         f'(identificado(a) como: {contrato.identificacao_local or "a ser definido"}), '
         f'para acomodação do animal descrito acima, pelo valor mensal de '
         f'R$ {contrato.valor_mensal:,.2f}, com vencimento no dia {contrato.dia_vencimento} de cada mês.'),
        ('2ª', 'DO PRAZO', f'O presente contrato tem início em {contrato.data_inicio.strftime("%d/%m/%Y")} '
         f'e término em {contrato.data_fim.strftime("%d/%m/%Y") if contrato.data_fim else "prazo indeterminado"}, '
         f'podendo ser rescindido por qualquer das partes mediante aviso prévio de 30 (trinta) dias.'),
        ('3ª', 'DO PAGAMENTO', f'O pagamento do aluguel deverá ser efetuado até o dia {contrato.dia_vencimento} '
         f'de cada mês. O atraso no pagamento implicará multa de 2% sobre o valor em atraso e '
         f'juros moratórios de 1% ao mês.'),
        ('4ª', 'DOS INSUMOS', 'Os valores de ração, feno, serragem e demais insumos fornecidos pela cocheira '
         'serão cobrados separadamente, com base no consumo real registrado e incluídos nas faturas mensais.'),
        ('5ª', 'DOS CUIDADOS', 'O CONTRATANTE é responsável pelos cuidados veterinários, vacinas e demais '
         'necessidades de saúde do animal. A cocheira não se responsabiliza por doenças ou acidentes '
         'ocorridos com o animal durante o período de estadia.'),
        ('6ª', 'DA RESCISÃO', 'O descumprimento de qualquer cláusula deste contrato por qualquer das partes '
         'poderá ensejar rescisão imediata, sem prejuízo das penalidades cabíveis.'),
    ]

    for num, titulo, texto in clausulas:
        story.append(Paragraph(
            f'<b>Cláusula {num} – {titulo}:</b> {texto}',
            style_body
        ))

    # Cláusulas extras
    if contrato.clausulas_extras:
        story.append(Paragraph('<b>Cláusulas Adicionais:</b>', style_body))
        story.append(Paragraph(contrato.clausulas_extras, style_body))

    # Local e data
    story.append(Spacer(1, 1*cm))
    hoje = datetime.date.today()
    cidade = cliente.cidade or '_______________'
    story.append(Paragraph(
        f'{cidade}, {hoje.day} de {_mes_extenso(hoje.month)} de {hoje.year}.',
        style_body
    ))

    # Assinaturas
    story.append(Spacer(1, 1.5*cm))
    assinaturas = [
        ['_________________________________', '', '_________________________________'],
        ['CONTRATANTE', '', 'COCHEIRA (CONTRATADA)'],
        [cliente.nome, '', ''],
        [f'CPF: {cliente.cpf}', '', ''],
    ]
    table_ass = Table(assinaturas, colWidths=[7*cm, 3*cm, 7*cm])
    table_ass.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(table_ass)

    doc.build(story)
    buffer.seek(0)
    return buffer


def _mes_extenso(mes):
    meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
             'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    return meses[mes - 1]
