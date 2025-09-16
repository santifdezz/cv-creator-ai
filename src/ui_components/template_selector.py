"""
Selector de Plantillas (TemplateSelector) - CV Creator AI
Permite seleccionar entre diferentes plantillas de CV
"""

import gradio as gr
from typing import Dict, Any, List, Tuple


class TemplateSelector:
    """Componente selector de plantillas"""
    
    def __init__(self):
        self.component = None
        self.templates = [
            ("🎨 Moderna - Diseño limpio y profesional", "modern"),
            ("👔 Ejecutiva - Estilo tradicional para puestos senior", "executive"),  
            ("🌈 Creativa - Para diseñadores y profesionales creativos", "creative"),
            ("💻 Técnica - Optimizada para desarrolladores y IT", "technical")
        ]
    
    def render(self) -> gr.Dropdown:
        """Renderizar el selector de plantillas"""
        
        with gr.Group():
            gr.Markdown("### 🎨 **Selecciona tu Plantilla**")
            
            self.component = gr.Dropdown(
                choices=self.templates,
                value="modern",
                label="Plantilla de CV",
                info="🎯 Elige según tu sector profesional",
                interactive=True,
                elem_id="template_selector"
            )
            
            # Vista previa de plantillas
            gr.HTML("""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px;">
                <div style="padding: 8px; border: 1px solid #e5e7eb; border-radius: 6px; text-align: center; font-size: 0.8rem;">
                    <strong style="color: #2563eb;">🎨 Moderna</strong>
                </div>
                <div style="padding: 8px; border: 1px solid #e5e7eb; border-radius: 6px; text-align: center; font-size: 0.8rem;">
                    <strong style="color: #374151;">👔 Ejecutiva</strong>
                </div>
                <div style="padding: 8px; border: 1px solid #e5e7eb; border-radius: 6px; text-align: center; font-size: 0.8rem;">
                    <strong style="color: #7c3aed;">🌈 Creativa</strong>
                </div>
                <div style="padding: 8px; border: 1px solid #e5e7eb; border-radius: 6px; text-align: center; font-size: 0.8rem;">
                    <strong style="color: #16a34a;">💻 Técnica</strong>
                </div>
            </div>
            """)
        
        return self.component
    
    def get_selected_template(self) -> str:
        """Obtener plantilla seleccionada"""
        return self.component.value if self.component else "modern"