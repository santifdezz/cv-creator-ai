"""
Componente de Habilidades y Competencias - CV Creator AI
Maneja habilidades, idiomas, certificaciones y proyectos
"""

import gradio as gr
from typing import Dict, List, Any


class SkillsComponent:
    """Componente para manejar habilidades, idiomas y información adicional"""
    
    def __init__(self):
        self.components = {}
    
    def render(self) -> Dict[str, Any]:
        """Renderizar el componente de habilidades y competencias"""
        
        gr.Markdown("## 🎯 **Habilidades y Competencias**")
        
        # Habilidades técnicas
        with gr.Group():
            gr.Markdown("### 🛠️ **Habilidades Técnicas**")
            
            self.components['habilidades'] = gr.Textbox(
                label="Habilidades y Competencias",
                placeholder="""• Lenguajes: JavaScript, Python, Java, TypeScript
• Frontend: React, Vue.js, HTML5, CSS3, Sass
• Backend: Node.js, Express, Django, REST APIs
• Bases de datos: MongoDB, PostgreSQL, MySQL
• DevOps: Docker, AWS, Git, CI/CD
• Metodologías: Scrum, Agile, TDD""",
                info="Organiza por categorías para mejor lectura",
                lines=6
            )
        
        # Idiomas
        with gr.Group():
            gr.Markdown("### 🌍 **Idiomas**")
            
            self.components['idiomas'] = gr.Textbox(
                label="Idiomas",
                placeholder="""• Español - Nativo
• Inglés - Avanzado (C1)
• Francés - Intermedio (B2)""",
                info="Incluye el nivel según el Marco Común Europeo",
                lines=3
            )
        
        # Información adicional consolidada
        with gr.Group():
            gr.Markdown("### ✨ **Información Adicional**")
            
            with gr.Accordion("📋 Certificaciones", open=False):
                self.components['certificaciones'] = gr.Textbox(
                    label="Certificaciones",
                    placeholder="• AWS Solutions Architect (2023)\n• Google Analytics Certified (2022)\n• Scrum Master Certified (2021)",
                    info="Certificaciones profesionales relevantes",
                    lines=3
                )
            
            with gr.Accordion("🚀 Proyectos Destacados", open=False):
                self.components['proyectos'] = gr.Textbox(
                    label="Proyectos",
                    placeholder="• E-commerce Platform - React + Node.js\n• Task Management App - Vue.js + Firebase\n• API RESTful - Python + Django",
                    info="Proyectos que demuestren tus habilidades",
                    lines=3
                )
        
        return self.components
    
    def get_inputs(self) -> List[Any]:
        """Retornar lista de inputs del componente"""
        return [
            self.components['habilidades'],
            self.components['idiomas'],
            self.components['certificaciones'],
            self.components['proyectos']
        ]
    
    def get_validation_handlers(self) -> Dict[str, Any]:
        """Retornar handlers de validación del componente"""
        return {}  # Este componente no tiene validaciones en tiempo real