"""
Generador Automático de CV con IA
==================================

Un generador de currículums profesionales que utiliza diferentes APIs de inteligencia 
artificial para optimizar el contenido y crear PDFs con diseño ATS-friendly.

Módulos principales:
- config: Configuración de APIs y modelos
- ai_service: Servicio de llamadas a APIs de IA
- content_generator: Generador de contenido sin IA (fallback)
- pdf_generator: Generador de PDFs profesionales
- utils: Utilidades y validaciones

Ejemplo de uso:
    from src.ai_service import AIService
    from src.pdf_generator import PDFGenerator
    
    ai_service = AIService()
    pdf_generator = PDFGenerator()
"""

__version__ = "1.0.0"
__author__ = "SantiFdezz"
__email__ = "santifdezseo@gmail.com"

# Importaciones principales para facilitar el uso
from .config import API_CONFIGS
from .ai_service import AIService
from .content_generator import ContentGenerator
from .pdf_generator import PDFGenerator
from .utils import validate_form_data, format_success_message

__all__ = [
    "API_CONFIGS",
    "AIService", 
    "ContentGenerator",
    "PDFGenerator",
    "validate_form_data",
    "format_success_message"
]