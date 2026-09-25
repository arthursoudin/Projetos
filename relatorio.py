import io
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

def gerar_relatorio( ordem_carga, data, operador, motorista, transportadora, placa, cpf, produtos):
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=12*mm, leftMargin=12*mm, 
        topMargin=15*mm, bottomMargin=15*mm
    )
    
    elementos = []
    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(name='Titulo', fontName='Helvetica-Bold', fontSize=15, alignment=TA_LEFT)
    estilo_texto = ParagraphStyle(name='Texto', fontName='Helvetica-Bold', fontSize=10, alignment=TA_LEFT)
    estilo_header = ParagraphStyle(name='Header', fontName='Helvetica-Bold', fontSize=10, alignment=TA_LEFT)

    # ==========================================
    # IMAGEM (LOGOTIPO)
    # ==========================================
    caminho_imagem = "logo_triangulo.png" 
    
    if os.path.exists(caminho_imagem):
        img_logo = Image(caminho_imagem, width=45*mm, height=18*mm)
    else:
        img_logo = Paragraph("<i>(Sem Logo)</i>", estilo_texto)

    # ==========================================
    # TRATAMENTO DOS DADOS DOS PRODUTOS
    # ==========================================
    produtos_dados = produtos[1:] if len(produtos) > 0 else []
    
    # Adicionado o 5º elemento vazio para completar as 5 colunas
    while len(produtos_dados) < 10:
        produtos_dados.append(["", "", "", "", ""])

    # ==========================================
    # CONSTRUÇÃO DA TABELA MESTRE (Sem Redespacho)
    # ==========================================
    dados_tabela = []
    
    dados_tabela.append([Paragraph("RELATORIO DE AVARIA OU FALTA DOCE MINEIRO", estilo_titulo), "", "", "", img_logo])
    dados_tabela.append(["", "", "", "", ""])
    
    dados_tabela.append([Paragraph(f"ORDEM DE CARGA: {ordem_carga}", estilo_texto), "", "", "", ""])
    
    data_str = data.strftime('%d/%m/%Y') if hasattr(data, 'strftime') else data
    dados_tabela.append([Paragraph(f"DATA DO RECEBIMENTO: {data_str}", estilo_texto), "", "", "", ""])
    dados_tabela.append([Paragraph(f"OPERADOR: {operador}", estilo_texto), "", "", "", ""])
    
    dados_tabela.append(["", "", "", "", ""])
    
    dados_tabela.append([
        Paragraph("<u>CÓDIGO</u>", estilo_header),
        Paragraph("<u>QUANTIDADE</u>", estilo_header),
        Paragraph("<u>PRODUTO</u>", estilo_header),
        Paragraph("<u>MOTIVO</u>", estilo_header),
        Paragraph("<u>NOTA FISCAL</u>", estilo_header)
    ])
    
    dados_tabela.append(["", "", "", "", ""])
    
    for p in produtos_dados:
        col0 = p[0] if len(p) > 0 else ""
        col1 = p[1] if len(p) > 1 else ""
        col2 = p[2] if len(p) > 2 else ""
        col3 = p[3] if len(p) > 3 else ""
        col4 = p[4] if len(p) > 4 else ""

        dados_tabela.append([
            Paragraph(str(col0), estilo_texto) if col0 else "",
            Paragraph(str(col1), estilo_texto) if col1 else "",
            Paragraph(str(col2), estilo_texto) if col2 else "",
            Paragraph(str(col3), estilo_texto) if col3 else "",
            Paragraph(str(col4), estilo_texto) if col4 else ""
        ])
        
    P = len(produtos_dados)
    
    # Índices corrigidos (-1 devido à remoção do redespacho)
    idx_barra_rodape = 8 + P
    idx_moto = 8 + P + 1
    
    dados_tabela.append(["", "", "", "", ""])
    
    dados_tabela.append([Paragraph("MOTORISTA:", estilo_texto), Paragraph(motorista, estilo_texto), "", "", ""])
    dados_tabela.append([Paragraph("PLACA:", estilo_texto), Paragraph(placa, estilo_texto), "", "", ""])
    dados_tabela.append([Paragraph("TRANPORTADOR:", estilo_texto), Paragraph(transportadora, estilo_texto), "", "", ""])
    dados_tabela.append([Paragraph("CPF:", estilo_texto), Paragraph(cpf, estilo_texto), "", "", ""])

    # ==========================================
    # LARGURA E ALTURA DA TABELA
    # ==========================================
    # Alturas corrigidas (removido um 7*mm do cabeçalho)
    alturas = [24*mm, 4*mm, 7*mm, 7*mm, 7*mm, 4*mm, 7*mm, 4*mm]
    alturas += [None] * P  
    alturas += [4*mm, None, None, None, None] 

    larguras_colunas = [36*mm, 28*mm, 63*mm, 35*mm, 30*mm] 

    tabela = Table(dados_tabela, colWidths=larguras_colunas, rowHeights=alturas)

    # ==========================================
    # ESTILIZAÇÃO DA TABELA
    # ==========================================
    estilo = [
        ('GRID', (0,1), (-1,-1), 1, colors.black),
        ('BOX', (0,0), (-1,0), 1, colors.black),

        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 2*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2*mm),
        
        ('SPAN', (0,0), (3,0)),
        ('ALIGN', (4,0), (4,0), 'RIGHT'),
        
        ('SPAN', (0,1), (-1,1)),
        ('BACKGROUND', (0,1), (-1,1), colors.lightgrey),
        
        # Índices de expansão ajustados (-1)
        ('SPAN', (0,2), (-1,2)),
        ('SPAN', (0,3), (-1,3)),
        ('SPAN', (0,4), (-1,4)),
        
        ('SPAN', (0,5), (-1,5)),
        ('BACKGROUND', (0,5), (-1,5), colors.lightgrey),
        
        ('SPAN', (0,7), (-1,7)),
        ('BACKGROUND', (0,7), (-1,7), colors.lightgrey),
        
        ('SPAN', (0,idx_barra_rodape), (-1,idx_barra_rodape)),
        ('BACKGROUND', (0,idx_barra_rodape), (-1,idx_barra_rodape), colors.lightgrey),
        
        ('SPAN', (1,idx_moto), (-1,idx_moto)),
        ('SPAN', (1,idx_moto+1), (-1,idx_moto+1)),
        ('SPAN', (1,idx_moto+2), (-1,idx_moto+2)),
        ('SPAN', (1,idx_moto+3), (-1,idx_moto+3)),
    ]
    
    tabela.setStyle(TableStyle(estilo))
    elementos.append(tabela)
    
    elementos.append(Spacer(1, 15*mm))
    
    # ==========================================
    # ASSINATURAS
    # ==========================================
    assinaturas = [
        ["___________________________________________", "___________________________________________"],
        ["CONFERENTE", "ASSINATURA E CPF DO MOTORISTA"]
    ]
    # Reduzi levemente o tamanho das colunas de assinatura para evitar overflow na margem direita
    tabela_assinaturas = Table(assinaturas, colWidths=[93*mm, 93*mm])
    tabela_assinaturas.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
    ]))
    
    elementos.append(tabela_assinaturas)

    doc.build(elementos)
    buffer.seek(0)
    
    return buffer