from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import PDI
from django.contrib import messages
import os
from django.conf import settings
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from django.template.loader import render_to_string
import pdfkit

# Configurar o caminho para o executável wkhtmltopdf
# Isso é necessário porque o pdfkit pode não encontrá-lo automaticamente em alguns ambientes
config = pdfkit.configuration(wkhtmltopdf="C:\Program Files\wkhtmltopdf\m\wkhtmltopdf.exe")

def formulario(request):
    """
    Exibe o formulário para preenchimento do PDI
    """
    return render(request, 'pdi_form/formulario.html')

def salvar_pdi(request):
    """
    Salva os dados do formulário no banco de dados
    """
    if request.method == 'POST':
        # Extrair dados do formulário
        nome = request.POST.get('nome')
        ra = request.POST.get('ra')
        curso = request.POST.get('curso')
        perfil = request.POST.get('perfil')
        competencias = request.POST.get('competencias')
        gaps = request.POST.get('gaps', '')
        linkedin = request.POST.get('linkedin')
        certificados = request.POST.get('certificados', '')
        inicio_jornada = request.POST.get('inicio_jornada', '')
        desenvolvimento_permanente = request.POST.get('desenvolvimento_permanente', '')
        jobs_desenvolvidos = request.POST.get('jobs_desenvolvidos', '')
        acoes_voluntarias = request.POST.get('acoes_voluntarias', '')
        
        # Extrair dados dos pitchs por semestre
        pitch_1_semestre = request.POST.get('pitch_1_semestre')
        pitch_2_semestre = request.POST.get('pitch_2_semestre')
        pitch_3_semestre = request.POST.get('pitch_3_semestre')
        pitch_4_semestre = request.POST.get('pitch_4_semestre')
        pitch_5_semestre = request.POST.get('pitch_5_semestre')
        pitch_6_semestre = request.POST.get('pitch_6_semestre')
        pitch_7_semestre = request.POST.get('pitch_7_semestre')
        pitch_8_semestre = request.POST.get('pitch_8_semestre')
        pitch_9_semestre = request.POST.get('pitch_9_semestre')
        pitch_10_semestre = request.POST.get('pitch_10_semestre')
        
        link_tcc = request.POST.get('link_tcc')
        
        # Criar ou atualizar o PDI
        pdi = PDI(
            nome=nome,
            ra=ra,
            curso=curso,
            perfil=perfil,
            competencias=competencias,
            gaps=gaps,
            linkedin=linkedin,
            certificados=certificados,
            inicio_jornada=inicio_jornada,
            desenvolvimento_permanente=desenvolvimento_permanente,
            jobs_desenvolvidos=jobs_desenvolvidos,
            pitch_1_semestre=pitch_1_semestre,
            pitch_2_semestre=pitch_2_semestre,
            pitch_3_semestre=pitch_3_semestre,
            pitch_4_semestre=pitch_4_semestre,
            pitch_5_semestre=pitch_5_semestre,
            pitch_6_semestre=pitch_6_semestre,
            pitch_7_semestre=pitch_7_semestre,
            pitch_8_semestre=pitch_8_semestre,
            pitch_9_semestre=pitch_9_semestre,
            pitch_10_semestre=pitch_10_semestre,
            link_tcc=link_tcc,
            acoes_voluntarias=acoes_voluntarias
        )
        pdi.save()
        
        
        if 'preview' in request.POST:
            print("--- 'preview' encontrado no POST! Redirecionando para visualizar_pdi... ---")
            return redirect('pdi_form:visualizar_pdi', pdi_id=pdi.id)
        else:
            print("--- 'preview' NÃO encontrado no POST. Redirecionando para gerar_pdf... ---")
            messages.success(request, 'PDI salvo com sucesso!')
            return redirect('pdi_form:gerar_pdf', pdi_id=pdi.id)

    
    # Se não for POST, redirecionar para o formulário
    return redirect('pdi_form:formulario')

def visualizar_pdi(request, pdi_id):
    """
    Visualiza os dados do PDI antes de gerar o PDF
    """
    pdi = get_object_or_404(PDI, id=pdi_id)
    return render(request, 'pdi_form/visualizar.html', {'pdi': pdi})

def gerar_pdf(request, pdi_id):
    """
    Gera o PDF personalizado com os dados do PDI usando template HTML estilizado
    """
    pdi = get_object_or_404(PDI, id=pdi_id)
    
    # Renderizar o template HTML com os dados do PDI
    html_string = render_to_string('pdi_form/pdf_template_estilizado.html', {'pdi': pdi})
    
    # Configurações para o wkhtmltopdf
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,
        'print-media-type': None,
    }
    
    try:
        # Gerar o PDF usando pdfkit, passando a configuração com o caminho do wkhtmltopdf
        pdf = pdfkit.from_string(html_string, False, options=options, configuration=config)
        
        # Criar a resposta HTTP com o PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="PDI-{pdi.nome}-{pdi.ra}.pdf"'
        
        return response
        
    except Exception as e:
        # Fallback para o método original se houver erro
        print(f"Erro ao gerar PDF com wkhtmltopdf: {e}")
        return gerar_pdf_reportlab(request, pdi_id)

def gerar_pdf_reportlab(request, pdi_id):
    """
    Gera o PDF personalizado com os dados do PDI usando ReportLab (método original)
    """
    pdi = get_object_or_404(PDI, id=pdi_id)
    
    # Criar um buffer para o PDF
    buffer = BytesIO()
    
    # Configurar o documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Estilos para o documento
    styles = getSampleStyleSheet()
    
    # Criar estilos personalizados com nomes únicos para evitar conflitos
    titulo_style = ParagraphStyle(
        name='PDITitle',  # Nome único para evitar conflito
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=colors.HexColor('#3498db')
    )
    
    heading2_style = ParagraphStyle(
        name='PDIHeading2',  # Nome único para evitar conflito
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.HexColor('#2c3e50')
    )
    
    section_title_style = ParagraphStyle(
        name='PDISectionTitle',  # Nome único para evitar conflito
        parent=styles['Normal'],
        fontSize=12,
        spaceBefore=6,
        spaceAfter=6,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#34495e')
    )
    
    normal_style = styles['Normal']
    
    center_style = ParagraphStyle(
        name='PDICenter',  # Nome único para evitar conflito
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=10
    )
    
    # Conteúdo do documento
    elements = []
    
    # Título
    elements.append(Paragraph("PLANO DE DESENVOLVIMENTO INDIVIDUAL PROFISSIONAL - PDI", titulo_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Informações pessoais
    info_data = [
        ["Nome:", pdi.nome],
        ["RA:", pdi.ra],
        ["Curso:", pdi.curso],
        ["Linkedin:", pdi.linkedin]
    ]
    info_table = Table(info_data, colWidths=[3*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 1*cm))
    
    # Perfil e Competências
    elements.append(Paragraph("PERFIL E COMPETÊNCIAS", heading2_style))
    elements.append(Paragraph("PERFIL COMPORTAMENTAL", section_title_style))
    elements.append(Paragraph(pdi.perfil.replace('\n', '<br/>'), normal_style))
    elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph("COMPETÊNCIAS", section_title_style))
    elements.append(Paragraph(pdi.competencias.replace('\n', '<br/>'), normal_style))
    elements.append(Spacer(1, 0.5*cm))
     
    # Resultados Alcançados
    elements.append(Paragraph("PROJETOS REALIZADOS", heading2_style))
    
    # Pitchs dos Projetos Integradores
    elements.append(Paragraph("PITCHS DOS PROJETOS INTEGRADORES", section_title_style))
    
    # Criar tabela para os pitchs
    pitchs_data = []
    
    # Primeira linha (semestres 1-5)
    row1 = []
    if pdi.pitch_1_semestre:
        row1.append(Paragraph("1° sem<br/>" + pdi.pitch_1_semestre.replace('\n', '<br/>'), normal_style))
    if pdi.pitch_2_semestre:
        row1.append(Paragraph("2° sem<br/>" + pdi.pitch_2_semestre.replace('\n', '<br/>'), normal_style))
    if pdi.pitch_3_semestre:
        row1.append(Paragraph("3° sem<br/>" + pdi.pitch_3_semestre.replace('\n', '<br/>'), normal_style))
    if pdi.pitch_4_semestre:
        row1.append(Paragraph("4° sem<br/>" + pdi.pitch_4_semestre.replace('\n', '<br/>'), normal_style))
    if pdi.pitch_5_semestre:
        row1.append(Paragraph("5° sem<br/>" + pdi.pitch_5_semestre.replace('\n', '<br/>'), normal_style))
    
    # Segunda linha (semestres 6-10)
    row2 = []
    if pdi.pitch_6_semestre:
        row2.append(Paragraph("6° sem<br/>" + pdi.pitch_6_semestre.replace('\n', '<br/>'), normal_style))
    if pdi.pitch_7_semestre:
        row2.append(Paragraph("7° sem<br/>" + pdi.pitch_7_semestre.replace('\n', '<br/>'), normal_style))
    if pdi.pitch_8_semestre:
        row2.append(Paragraph("8° sem<br/>" + pdi.pitch_8_semestre.replace('\n', '<br/>'), normal_style))
    if pdi.pitch_9_semestre:
        row2.append(Paragraph("9° sem<br/>" + pdi.pitch_9_semestre.replace('\n', '<br/>'), normal_style))
    if pdi.pitch_10_semestre:
        row2.append(Paragraph("10° sem<br/>" + pdi.pitch_10_semestre.replace('\n', '<br/>'), normal_style))
    
    # Adicionar linhas à tabela se tiverem conteúdo
    if row1:
        pitchs_data.append(row1)
    if row2:
        pitchs_data.append(row2)
    
    # Adicionar tabela de pitchs se houver dados
    if pitchs_data:
        col_width = 15*cm / max(len(row1) if row1 else 0, len(row2) if row2 else 0, 1)
        pitchs_table = Table(pitchs_data, colWidths=[col_width] * max(len(row1) if row1 else 0, len(row2) if row2 else 0, 1))
        pitchs_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(pitchs_table)
        elements.append(Spacer(1, 0.5*cm))
    
    if pdi.link_tcc:
        elements.append(Paragraph("LINK DO TCC", section_title_style))
        elements.append(Paragraph(pdi.link_tcc, normal_style))
        elements.append(Spacer(1, 0.5*cm))
    # Rodapé
    import datetime
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(f"PDI gerado em {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", center_style))
    
    # Construir o PDF
    doc.build(elements)
    
    # Obter o valor do buffer e criar a resposta HTTP
    pdf = buffer.getvalue()
    buffer.close()
    
    # Criar a resposta HTTP com o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PDI-{pdi.nome}-{pdi.ra}.pdf"'
    response.write(pdf)
    
    return response

