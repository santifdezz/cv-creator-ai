"""
UI Components Module for CV Generator
Componentes modulares y reutilizables para la interfaz de usuario
"""

from .components import (
    UIComponent,
    PersonalInfoComponent,
    RichTextComponent,
    DraggableSectionComponent,
    TemplateSelector
)

from .styles import ADVANCED_CSS
from .javascript import ADVANCED_JAVASCRIPT

__all__ = [
    'UIComponent',
    'PersonalInfoComponent', 
    'RichTextComponent',
    'DraggableSectionComponent',
    'TemplateSelector',
    'ADVANCED_CSS',
    'ADVANCED_JAVASCRIPT'
]