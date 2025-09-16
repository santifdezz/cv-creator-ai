"""
Componente de Sección Arrastrable (DraggableSectionComponent) - CV Creator AI
Permite crear secciones que se pueden reorganizar mediante drag-and-drop
"""

import gradio as gr
from typing import Dict, Any, Optional


class DraggableSectionComponent:
    """Componente de sección arrastrable"""
    
    def __init__(self, section_id: str, title: str, icon: str = "", 
                 content_component: Any = None):
        self.section_id = section_id
        self.title = title
        self.icon = icon
        self.content_component = content_component
        self.components = {}
    
    def render(self) -> Dict[str, Any]:
        """Renderizar la sección arrastrable"""
        
        # Crear grupo para la sección
        with gr.Group(elem_id=f"section_{self.section_id}", elem_classes=["draggable-section"]):
            # Header de la sección
            gr.HTML(f"""
            <div class="section-header" data-section="{self.section_id}">
                <span class="drag-handle">⋮⋮</span>
                <span class="section-icon">{self.icon}</span>
                <span class="section-title">{self.title}</span>
                <span class="section-toggle">📁</span>
            </div>
            """)
            
            # Contenido de la sección
            if self.content_component:
                if hasattr(self.content_component, 'render'):
                    # Si es un componente con método render
                    content_result = self.content_component.render()
                    if isinstance(content_result, dict):
                        self.components.update(content_result)
                    else:
                        # Es un componente gradio directo
                        component_name = getattr(self.content_component, 'elem_id', self.section_id)
                        self.components[component_name] = content_result
                else:
                    # Es un componente gradio directo
                    self.components[self.section_id] = self.content_component
        
        return self.components
    
    def get_section_data(self) -> Dict[str, Any]:
        """Obtener datos de la sección"""
        return {
            'id': self.section_id,
            'title': self.title,
            'icon': self.icon,
            'components': self.components
        }