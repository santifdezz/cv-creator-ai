"""
Generador de PDF para currículums profesionales

Este módulo se encarga de crear PDFs con diseño profesional y optimizado para ATS
utilizando ReportLab.
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import black, darkblue, grey
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import tempfile
from typing import Dict, Any

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para el PDF"""
        
        # Estilo para el nombre
        self.nombre_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=6,
            textColor=darkblue,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para información de contacto
        self.contacto_style = ParagraphStyle(
            'ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=grey
        )
        
        # Estilo para encabezados de sección
        self.seccion_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=16,
            textColor=darkblue,
            borderWidth=1,
            borderColor=darkblue,
            borderPadding=4,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para contenido normal
        self.contenido_style = ParagraphStyle(
            'Content',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=black,
            alignment=TA_LEFT
        )
        
        # Estilo para subsecciones
        self.subseccion_style = ParagraphStyle(
            'Subsection',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            spaceBefore=8,
            textColor=darkblue,
            fontName='Helvetica-Bold'
        )

    def create_cv_pdf(self, form_data: Dict[str, Any], ai_content: Dict[str, Any]) -> str:
        """
        Genera un PDF profesional del CV
        
        Args:
            form_data: Datos del formulario
            ai_content: Contenido generado por IA
            
        Returns:
            str: Ruta del archivo PDF generado
        """
        
        # Crear archivo temporal
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_filename = temp_file.name
        temp_file.close()
        
        # Configurar documento
        doc = SimpleDocTemplate(
            temp_filename,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Crear contenido del PDF
        story = []
        
        # Header - Nombre y contacto
        self._add_header(story, form_data)
        
        # Resumen profesional
        self._add_professional_summary(story, ai_content)
        
        # Experiencia laboral
        self._add_work_experience(story, ai_content)
        
        # Educación
        self._add_education(story, form_data)
        
        # Habilidades
        self._add_skills(story, ai_content)
        
        # Idiomas
        self._add_languages(story, form_data)
        
        # Generar PDF
        doc.build(story)
        
        return temp_filename

    def _add_header(self, story: list, form_data: Dict[str, Any]):
        """Añade el encabezado con nombre e información de contacto"""
        
        # Nombre
        story.append(Paragraph(form_data['nombre'].upper(), self.nombre_style))
        
        # Información de contacto en una línea
        contacto_info = []
        if form_data.get('email'):
            contacto_info.append(f"✉ {form_data['email']}")
        if form_data.get('telefono'):
            contacto_info.append(f"📞 {form_data['telefono']}")
        if form_data.get('ubicacion'):
            contacto_info.append(f"📍 {form_data['ubicacion']}")
        if form_data.get('linkedin'):
            contacto_info.append(f"🔗 {form_data['linkedin']}")
        
        if contacto_info:
            story.append(Paragraph(" | ".join(contacto_info), self.contacto_style))
        
        # Línea separadora
        story.append(Spacer(1, 0.2*inch))

    def _add_professional_summary(self, story: list, ai_content: Dict[str, Any]):
        """Añade el resumen profesional"""
        
        story.append(Paragraph("RESUMEN PROFESIONAL", self.seccion_style))
        story.append(Paragraph(ai_content['resumen_profesional'], self.contenido_style))

    def _add_work_experience(self, story: list, ai_content: Dict[str, Any]):
        """Añade la experiencia laboral"""
        
        if ai_content['experiencia_optimizada']:
            story.append(Paragraph("EXPERIENCIA PROFESIONAL", self.seccion_style))
            
            for exp in ai_content['experiencia_optimizada']:
                # Título del puesto y empresa
                puesto_empresa = f"<b>{exp['puesto']}</b> - {exp['empresa']}"
                if exp.get('periodo'):
                    puesto_empresa += f" ({exp['periodo']})"
                
                story.append(Paragraph(puesto_empresa, self.subseccion_style))
                
                # Logros y responsabilidades
                for logro in exp['descripcion']:
                    story.append(Paragraph(f"• {logro}", self.contenido_style))

    def _add_education(self, story: list, form_data: Dict[str, Any]):
        """Añade la educación"""
        
        if form_data.get('educacion'):
            story.append(Paragraph("EDUCACIÓN", self.seccion_style))
            educacion_lines = form_data['educacion'].split('\n')
            for line in educacion_lines:
                if line.strip():
                    story.append(Paragraph(f"• {line.strip()}", self.contenido_style))

    def _add_skills(self, story: list, ai_content: Dict[str, Any]):
        """Añade las habilidades organizadas"""
        
        habilidades = ai_content['habilidades_organizadas']
        if any(habilidades.values()):
            story.append(Paragraph("HABILIDADES Y COMPETENCIAS", self.seccion_style))
            
            if habilidades.get('tecnicas'):
                story.append(Paragraph("<b>Habilidades Técnicas:</b>", self.subseccion_style))
                story.append(Paragraph(", ".join(habilidades['tecnicas']), self.contenido_style))
            
            if habilidades.get('herramientas'):
                story.append(Paragraph("<b>Herramientas y Software:</b>", self.subseccion_style))
                story.append(Paragraph(", ".join(habilidades['herramientas']), self.contenido_style))
            
            if habilidades.get('blandas'):
                story.append(Paragraph("<b>Habilidades Interpersonales:</b>", self.subseccion_style))
                story.append(Paragraph(", ".join(habilidades['blandas']), self.contenido_style))

    def _add_languages(self, story: list, form_data: Dict[str, Any]):
        """Añade los idiomas"""
        
        if form_data.get('idiomas'):
            story.append(Paragraph("IDIOMAS", self.seccion_style))
            idiomas_lines = form_data['idiomas'].split('\n')
            for line in idiomas_lines:
                if line.strip():
                    story.append(Paragraph(f"• {line.strip()}", self.contenido_style))