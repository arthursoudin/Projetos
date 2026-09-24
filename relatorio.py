import io
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

def gerar_relatorio(redespacho, ordem_carga, data, operador, motorista, transportadora, placa, cpf, produtos):
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
    produtos_dados = produtos[1:] 
    
    while len(produtos_dados) < 10:
        produtos_dados.append(["", "", "", ""])

    # ==========================================
    # CONSTRUÇÃO DA TABELA MESTRE
    # ==========================================
    dados_tabela = []
    
    dados_tabela.append([Paragraph("RELATORIO DE AVARIA OU FALTA DOCE MINEIRO", estilo_titulo), "", "", img_logo])
    
    dados_tabela.append(["", "", "", ""])
    
    dados_tabela.append([Paragraph(f"REDESPACHO: {redespacho}", estilo_texto), "", "", ""])
    dados_tabela.append([Paragraph(f"ORDEM DE CARGA: {ordem_carga}", estilo_texto), "", "", ""])
    
    data_str = data.strftime('%d/%m/%Y') if hasattr(data, 'strftime') else data
    dados_tabela.append([Paragraph(f"DATA DO RECEBIMENTO: {data_str}", estilo_texto), "", "", ""])
    dados_tabela.append([Paragraph(f"OPERADOR: {operador}", estilo_texto), "", "", ""])
    
    dados_tabela.append(["", "", "", ""])
    
    dados_tabela.append([
        Paragraph("<u>QUANTIDADE</u>", estilo_header),
        Paragraph("<u>PRODUTO</u>", estilo_header),
        Paragraph("<u>MOTIVO</u>", estilo_header),
        Paragraph("<u>NOTA FISCAL</u>", estilo_header)
    ])
    
    dados_tabela.append(["", "", "", ""])
    
    for p in produtos_dados:
        dados_tabela.append([
            Paragraph(str(p[0]), estilo_texto) if p[0] else "",
            Paragraph(str(p[1]), estilo_texto) if p[1] else "",
            Paragraph(str(p[2]), estilo_texto) if p[2] else "",
            Paragraph(str(p[3]), estilo_texto) if p[3] else ""
        ])
        
    P = len(produtos_dados)
    idx_barra_rodape = 9 + P
    idx_moto = 9 + P + 1
    
    dados_tabela.append(["", "", "", ""])
    
    dados_tabela.append([Paragraph("MOTORISTA:", estilo_texto), Paragraph(motorista, estilo_texto), "", ""])
    dados_tabela.append([Paragraph("PLACA:", estilo_texto), Paragraph(placa, estilo_texto), "", ""])
    dados_tabela.append([Paragraph("TRANPORTADOR:", estilo_texto), Paragraph(transportadora, estilo_texto), "", ""])
    dados_tabela.append([Paragraph("CPF:", estilo_texto), Paragraph(cpf, estilo_texto), "", ""])

    alturas = [22*mm, 4*mm, 7*mm, 7*mm, 7*mm, 7*mm, 4*mm, 7*mm, 4*mm]
    alturas += [7*mm] * P
    alturas += [4*mm, 7*mm, 7*mm, 7*mm, 7*mm]

    tabela = Table(dados_tabela, colWidths=[45*mm, 70*mm, 40*mm, 35*mm], rowHeights=alturas)

    # ==========================================
    # ESTILIZAÇÃO DA TABELA
    # ==========================================
    estilo = [
        # Grelha global a partir da linha 1 (ignora a linha do título)
        ('GRID', (0,1), (-1,-1), 1, colors.black),
        
        # Desenha apenas a caixa exterior na linha do título (sem linha vertical no meio)
        ('BOX', (0,0), (-1,0), 1, colors.black),

        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 2*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 2*mm),
        
        ('SPAN', (0,0), (2,0)),
        ('ALIGN', (3,0), (3,0), 'RIGHT'),
        
        ('SPAN', (0,1), (-1,1)),
        ('BACKGROUND', (0,1), (-1,1), colors.lightgrey),
        
        ('SPAN', (0,2), (-1,2)),
        ('SPAN', (0,3), (-1,3)),
        ('SPAN', (0,4), (-1,4)),
        ('SPAN', (0,5), (-1,5)),
        
        ('SPAN', (0,6), (-1,6)),
        ('BACKGROUND', (0,6), (-1,6), colors.lightgrey),
        
        ('SPAN', (0,8), (-1,8)),
        ('BACKGROUND', (0,8), (-1,8), colors.lightgrey),
        
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
    tabela_assinaturas = Table(assinaturas, colWidths=[95*mm, 95*mm])
    tabela_assinaturas.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
    ]))
    
    elementos.append(tabela_assinaturas)

    doc.build(elementos)
    buffer.seek(0)
    
    return buffer