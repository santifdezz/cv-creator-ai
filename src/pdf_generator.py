"""
Generador de PDF para currículums profesionales con múltiples plantillas

Este módulo se encarga de crear PDFs con diseño profesional y optimizado para ATS
utilizando ReportLab. Incluye múltiples plantillas personalizables.
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import black, darkblue, grey, blue, green, red, purple
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import tempfile
from typing import Dict, Any
from abc import ABC, abstractmethod

class CVTemplate(ABC):
    """Clase base abstracta para plantillas de CV"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    @abstractmethod
    def _setup_custom_styles(self):
        """Configura estilos específicos de la plantilla"""
        pass
    
    @abstractmethod
    def create_content(self, form_data: Dict[str, Any], ai_content: Dict[str, Any]) -> list:
        """Crea el contenido del CV usando la plantilla específica"""
        pass

class ModernTemplate(CVTemplate):
    """Plantilla moderna y minimalista"""
    
    def _setup_custom_styles(self):
        # Estilo para el nombre - moderno y limpio
        self.nombre_style = ParagraphStyle(
            'ModernTitle',
            parent=self.styles['Heading1'],
            fontSize=26,
            spaceAfter=8,
            textColor=darkblue,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        # Información de contacto elegante
        self.contacto_style = ParagraphStyle(
            'ModernContact',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=20,
            textColor=grey,
            fontName='Helvetica'
        )
        
        # Encabezados de sección con línea moderna
        self.seccion_style = ParagraphStyle(
            'ModernSection',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=18,
            textColor=darkblue,
            fontName='Helvetica-Bold',
            borderWidth=2,
            borderColor=darkblue,
            borderPadding=6,
            leftIndent=0
        )
        
        # Contenido limpio
        self.contenido_style = ParagraphStyle(
            'ModernContent',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=black,
            alignment=TA_LEFT,
            leftIndent=10
        )
        
        self.subseccion_style = ParagraphStyle(
            'ModernSubsection',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            spaceBefore=8,
            textColor=darkblue,
            fontName='Helvetica-Bold',
            leftIndent=10
        )
    
    def create_content(self, form_data: Dict[str, Any], ai_content: Dict[str, Any]) -> list:
        """Implementación requerida por la clase abstracta"""
        return []

class ExecutiveTemplate(CVTemplate):
    """Plantilla ejecutiva y formal"""
    
    def _setup_custom_styles(self):
        # Estilo ejecutivo - centrado y formal
        self.nombre_style = ParagraphStyle(
            'ExecutiveTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=6,
            textColor=black,
            alignment=TA_CENTER,
            fontName='Times-Bold'
        )
        
        self.contacto_style = ParagraphStyle(
            'ExecutiveContact',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=black,
            fontName='Times-Roman'
        )
        
        self.seccion_style = ParagraphStyle(
            'ExecutiveSection',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=16,
            textColor=black,
            fontName='Times-Bold',
            alignment=TA_CENTER,
            borderWidth=1,
            borderColor=black
        )
        
        self.contenido_style = ParagraphStyle(
            'ExecutiveContent',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            textColor=black,
            alignment=TA_LEFT,
            fontName='Times-Roman'
        )
        
        self.subseccion_style = ParagraphStyle(
            'ExecutiveSubsection',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            spaceBefore=8,
            textColor=black,
            fontName='Times-Bold'
        )
    
    def create_content(self, form_data: Dict[str, Any], ai_content: Dict[str, Any]) -> list:
        """Implementación requerida por la clase abstracta"""
        return []

class CreativeTemplate(CVTemplate):
    """Plantilla creativa para diseñadores"""
    
    def _setup_custom_styles(self):
        # Estilo creativo con colores
        self.nombre_style = ParagraphStyle(
            'CreativeTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            spaceAfter=8,
            textColor=purple,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        self.contacto_style = ParagraphStyle(
            'CreativeContact',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=20,
            textColor=blue,
            fontName='Helvetica'
        )
        
        self.seccion_style = ParagraphStyle(
            'CreativeSection',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=18,
            textColor=purple,
            fontName='Helvetica-Bold',
            borderWidth=3,
            borderColor=purple
        )
        
        self.contenido_style = ParagraphStyle(
            'CreativeContent',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=black,
            alignment=TA_LEFT
        )
        
        self.subseccion_style = ParagraphStyle(
            'CreativeSubsection',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            spaceBefore=8,
            textColor=blue,
            fontName='Helvetica-Bold'
        )
    
    def create_content(self, form_data: Dict[str, Any], ai_content: Dict[str, Any]) -> list:
        """Implementación requerida por la clase abstracta"""
        return []

class TechnicalTemplate(CVTemplate):
    """Plantilla técnica para desarrolladores"""
    
    def _setup_custom_styles(self):
        # Estilo técnico - limpio y estructurado
        self.nombre_style = ParagraphStyle(
            'TechTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=8,
            textColor=green,
            alignment=TA_LEFT,
            fontName='Courier-Bold'
        )
        
        self.contacto_style = ParagraphStyle(
            'TechContact',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT,
            spaceAfter=20,
            textColor=grey,
            fontName='Courier'
        )
        
        self.seccion_style = ParagraphStyle(
            'TechSection',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=16,
            textColor=green,
            fontName='Courier-Bold',
            borderWidth=1,
            borderColor=green,
            leftIndent=20
        )
        
        self.contenido_style = ParagraphStyle(
            'TechContent',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=6,
            textColor=black,
            alignment=TA_LEFT,
            fontName='Courier',
            leftIndent=20
        )
        
        self.subseccion_style = ParagraphStyle(
            'TechSubsection',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            spaceBefore=8,
            textColor=green,
            fontName='Courier-Bold',
            leftIndent=20
        )
    
    def create_content(self, form_data: Dict[str, Any], ai_content: Dict[str, Any]) -> list:
        """Implementación requerida por la clase abstracta"""
        return []

class PDFGenerator:
    """Generador principal de PDFs con soporte para múltiples plantillas"""
    
    def __init__(self):
        self.templates = {
            'modern': ModernTemplate(),
            'executive': ExecutiveTemplate(), 
            'creative': CreativeTemplate(),
            'technical': TechnicalTemplate()
        }
        # Compatibilidad hacia atrás - usar plantilla moderna por defecto
        self.default_template = self.templates['modern']
        self._setup_legacy_styles()
    
    def _setup_legacy_styles(self):
        """Mantiene compatibilidad con el código existente"""
        template = self.default_template
        self.styles = template.styles
        self.nombre_style = template.nombre_style
        self.contacto_style = template.contacto_style
        self.seccion_style = template.seccion_style
        self.contenido_style = template.contenido_style
        self.subseccion_style = template.subseccion_style

    def create_cv_pdf(self, form_data: Dict[str, Any], ai_content: Dict[str, Any], template: str = 'modern') -> str:
        """
        Genera un PDF profesional del CV con la plantilla especificada
        
        Args:
            form_data: Datos del formulario
            ai_content: Contenido generado por IA
            template: Nombre de la plantilla ('modern', 'executive', 'creative', 'technical')
            
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
        
        # Seleccionar plantilla
        selected_template = self.templates.get(template, self.default_template)
        
        # Crear contenido usando la plantilla seleccionada
        story = self._create_universal_content(form_data, ai_content, selected_template)
        
        # Generar PDF
        doc.build(story)
        
        return temp_filename
    
    def _create_universal_content(self, form_data: Dict[str, Any], ai_content: Dict[str, Any], template: CVTemplate) -> list:
        """Crea contenido universal compatible con todas las plantillas"""
        
        story = []
        
        # Header - Nombre y contacto
        self._add_header(story, form_data, template)
        
        # Resumen profesional
        self._add_professional_summary(story, ai_content, template)
        
        # Experiencia laboral
        self._add_work_experience(story, ai_content, template)
        
        # Educación
        self._add_education(story, form_data, template)
        
        # Habilidades
        self._add_skills(story, ai_content, template)
        
        # Idiomas
        self._add_languages(story, form_data, template)
        
        return story

    def _add_header(self, story: list, form_data: Dict[str, Any], template: CVTemplate):
        """Añade el encabezado con nombre e información de contacto"""
        
        # Nombre
        story.append(Paragraph(form_data['nombre'].upper(), template.nombre_style))
        
        # Información de contacto
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
            # Para plantillas técnicas y creativas, mostrar contacto en líneas separadas
            if isinstance(template, (TechnicalTemplate, CreativeTemplate)):
                for info in contacto_info:
                    story.append(Paragraph(info, template.contacto_style))
            else:
                # Para plantillas moderna y ejecutiva, en una línea
                story.append(Paragraph(" | ".join(contacto_info), template.contacto_style))
        
        # Línea separadora
        story.append(Spacer(1, 0.2*inch))

    def _add_professional_summary(self, story: list, ai_content: Dict[str, Any], template: CVTemplate):
        """Añade el resumen profesional"""
        
        story.append(Paragraph("RESUMEN PROFESIONAL", template.seccion_style))
        story.append(Paragraph(ai_content['resumen_profesional'], template.contenido_style))

    def _add_work_experience(self, story: list, ai_content: Dict[str, Any], template: CVTemplate):
        """Añade la experiencia laboral"""
        
        if ai_content['experiencia_optimizada']:
            story.append(Paragraph("EXPERIENCIA PROFESIONAL", template.seccion_style))
            
            for exp in ai_content['experiencia_optimizada']:
                # Título del puesto y empresa
                puesto_empresa = f"<b>{exp['puesto']}</b> - {exp['empresa']}"
                if exp.get('periodo'):
                    puesto_empresa += f" ({exp['periodo']})"
                
                story.append(Paragraph(puesto_empresa, template.subseccion_style))
                
                # Logros y responsabilidades
                for logro in exp['descripcion']:
                    story.append(Paragraph(f"• {logro}", template.contenido_style))

    def _add_education(self, story: list, form_data: Dict[str, Any], template: CVTemplate):
        """Añade la educación"""
        
        if form_data.get('educacion'):
            story.append(Paragraph("EDUCACIÓN", template.seccion_style))
            educacion_lines = form_data['educacion'].split('\n')
            for line in educacion_lines:
                if line.strip():
                    story.append(Paragraph(f"• {line.strip()}", template.contenido_style))

    def _add_skills(self, story: list, ai_content: Dict[str, Any], template: CVTemplate):
        """Añade las habilidades organizadas"""
        
        habilidades = ai_content['habilidades_organizadas']
        if any(habilidades.values()):
            story.append(Paragraph("HABILIDADES Y COMPETENCIAS", template.seccion_style))
            
            if habilidades.get('tecnicas'):
                story.append(Paragraph("<b>Habilidades Técnicas:</b>", template.subseccion_style))
                story.append(Paragraph(", ".join(habilidades['tecnicas']), template.contenido_style))
            
            if habilidades.get('herramientas'):
                story.append(Paragraph("<b>Herramientas y Software:</b>", template.subseccion_style))
                story.append(Paragraph(", ".join(habilidades['herramientas']), template.contenido_style))
            
            if habilidades.get('blandas'):
                story.append(Paragraph("<b>Habilidades Interpersonales:</b>", template.subseccion_style))
                story.append(Paragraph(", ".join(habilidades['blandas']), template.contenido_style))

    def _add_languages(self, story: list, form_data: Dict[str, Any], template: CVTemplate):
        """Añade los idiomas"""
        
        if form_data.get('idiomas'):
            story.append(Paragraph("IDIOMAS", template.seccion_style))
            idiomas_lines = form_data['idiomas'].split('\n')
            for line in idiomas_lines:
                if line.strip():
                    story.append(Paragraph(f"• {line.strip()}", template.contenido_style))
    
    def get_available_templates(self) -> Dict[str, str]:
        """Retorna las plantillas disponibles con sus descripciones"""
        return {
            'modern': '🎨 Moderna y Minimalista - Diseño limpio y profesional',
            'executive': '👔 Ejecutiva y Formal - Estilo tradicional para puestos senior',
            'creative': '🌈 Creativa y Colorida - Para diseñadores y profesionales creativos',
            'technical': '💻 Técnica y Estructurada - Optimizada para desarrolladores y IT'
        }