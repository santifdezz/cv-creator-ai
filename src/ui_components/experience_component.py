"""
Componente de Experiencia Profesional - CV Creator AI
Maneja toda la información de experiencia laboral y educación
"""

import gradio as gr
from typing import Dict, List, Any


class ExperienceComponent:
    """Componente para manejar experiencia profesional y educación"""
    
    def __init__(self):
        self.components = {}
    
    def render(self) -> Dict[str, Any]:
        """Renderizar el componente de experiencia profesional"""
        
        gr.Markdown("## 💼 **Experiencia Profesional**")
        
        # Perfil profesional
        with gr.Group():
            gr.Markdown("### 🎯 **Objetivo Profesional**")
            
            self.components['objetivo'] = gr.Textbox(
                label="Describe tu objetivo",
                placeholder="Ej: Desarrollador Full Stack especializado en React y Node.js buscando liderar equipos de desarrollo en una startup tecnológica",
                info="Esto mejora significativamente la optimización ATS",
                lines=3
            )
            
            self.components['experiencia_anos'] = gr.Dropdown(
                choices=["Sin experiencia", "0-1 años", "2-3 años", "4-5 años", "6-10 años", "10+ años"],
                label="Años de Experiencia",
                info="Selecciona tu rango de experiencia",
                value="2-3 años"
            )
        
        # Experiencia laboral
        with gr.Group():
            gr.Markdown("### 💼 **Historial Laboral**")
            
            self.components['experiencia_laboral'] = gr.Textbox(
                label="Experiencia Laboral",
                placeholder="""• Desarrollador Senior - TechCorp (2020-2024)
  - Desarrollo de aplicaciones web con React y Node.js
  - Liderazgo de equipo de 3 desarrolladores
  - Implementación de metodologías ágiles

• Desarrollador Junior - StartupXYZ (2018-2020)
  - Desarrollo frontend con JavaScript y Vue.js
  - Colaboración en proyectos de e-commerce""",
                info="Usa viñetas (•) para mejor formato. Incluye logros específicos.",
                lines=8
            )
        
        # Educación
        with gr.Group():
            gr.Markdown("### 🎓 **Formación Académica**")
            
            self.components['educacion'] = gr.Textbox(
                label="Educación y Certificaciones",
                placeholder="""• Grado en Ingeniería Informática - Universidad Complutense Madrid (2014-2018)
• Máster en Desarrollo Web - UNIR (2019-2020)
• Certificación AWS Solutions Architect (2023)
• Curso Advanced React - Platzi (2022)""",
                info="Incluye títulos, certificaciones, cursos relevantes",
                lines=6
            )
        
        return self.components
    
    def get_inputs(self) -> List[Any]:
        """Retornar lista de inputs del componente"""
        return [
            self.components['objetivo'],
            self.components['experiencia_anos'],
            self.components['experiencia_laboral'],
            self.components['educacion']
        ]
    
    def get_validation_handlers(self) -> Dict[str, Any]:
        """Retornar handlers de validación del componente"""
        return {}  # Este componente no tiene validaciones en tiempo real