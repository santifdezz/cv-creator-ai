"""
Componente de Texto Rico (RichTextComponent) - CV Creator AI
Editor de texto avanzado con capacidades WYSIWYG
"""

import gradio as gr
from typing import Dict, Any, Optional


class RichTextComponent:
    """Componente de editor de texto rico"""
    
    def __init__(self, label: str = "Texto", placeholder: str = "", info: str = "", 
                 elem_id: str = "", lines: int = 3):
        self.label = label
        self.placeholder = placeholder
        self.info = info
        self.elem_id = elem_id
        self.lines = lines
        self.component = None
    
    def render(self) -> gr.Textbox:
        """Renderizar el componente de texto rico"""
        self.component = gr.Textbox(
            label=self.label,
            placeholder=self.placeholder,
            info=self.info,
            lines=self.lines,
            elem_id=self.elem_id,
            interactive=True
        )
        return self.component
    
    def get_value(self) -> str:
        """Obtener valor del componente"""
        return self.component.value if self.component else ""