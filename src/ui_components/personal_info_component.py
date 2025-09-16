"""
Componente de Información Personal - CV Creator AI
Incluye validaciones en tiempo real y todos los campos del app.py original
"""

import gradio as gr
from typing import Dict, List, Any, Tuple
from ..utils import validate_email, validate_phone, validate_linkedin, clean_text


class PersonalInfoComponent:
    """Componente para manejar toda la información personal del usuario"""
    
    def __init__(self):
        self.components = {}
        self.validation_components = {}
    
    def render(self) -> Dict[str, Any]:
        """Renderizar el componente de información personal"""
        
        gr.Markdown("## 👤 **Información Personal**")
        
        # Información básica
        with gr.Group():
            gr.Markdown("### ✨ **Datos Básicos** *(Obligatorio)*")
            
            self.components['nombre'] = gr.Textbox(
                label="Nombre Completo *",
                placeholder="Ej: María García López",
                info="Tu nombre completo como aparecerá en el CV",
                lines=1,
                elem_id="nombre_input"
            )
            
            self.components['email'] = gr.Textbox(
                label="Email *",
                placeholder="maria.garcia@email.com",
                info="Email profesional preferiblemente",
                lines=1,
                elem_id="email_input"
            )
            self.validation_components['email_validation'] = gr.HTML("", elem_id="email_validation")
            
            self.components['telefono'] = gr.Textbox(
                label="Teléfono *",
                placeholder="+34 666 123 456",
                info="Con código de país",
                lines=1,
                elem_id="telefono_input"
            )
            self.validation_components['phone_validation'] = gr.HTML("", elem_id="phone_validation")
            
            with gr.Row():
                self.components['linkedin'] = gr.Textbox(
                    label="LinkedIn",
                    placeholder="linkedin.com/in/maria-garcia",
                    info="Tu perfil profesional",
                    lines=1,
                    elem_id="linkedin_input"
                )
                self.components['ubicacion'] = gr.Textbox(
                    label="Ubicación",
                    placeholder="Madrid, España",
                    info="Ciudad donde resides",
                    lines=1,
                    elem_id="ubicacion_input"
                )
            
            self.validation_components['linkedin_validation'] = gr.HTML("", elem_id="linkedin_validation")
        
        # Selector de plantilla CV
        with gr.Group():
            gr.Markdown("### 🎨 **Diseño de tu CV**")
            
            template_choices = [
                ("🎨 Moderna - Diseño limpio y profesional", "modern"),
                ("👔 Ejecutiva - Estilo tradicional para puestos senior", "executive"),  
                ("🌈 Creativa - Para diseñadores y profesionales creativos", "creative"),
                ("💻 Técnica - Optimizada para desarrolladores y IT", "technical")
            ]
            
            self.components['template_selector'] = gr.Dropdown(
                choices=template_choices,
                value="modern",
                label="Plantilla de CV",
                info="🎯 Elige según tu sector profesional",
                interactive=True
            )
            
            # Vista previa compacta de plantillas
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
        
        return {**self.components, **self.validation_components}
    
    def get_inputs(self) -> List[Any]:
        """Retornar lista de inputs del componente"""
        return [
            self.components['nombre'],
            self.components['email'],
            self.components['telefono'],
            self.components['linkedin'],
            self.components['ubicacion'],
            self.components['template_selector']
        ]
    
    def get_validation_handlers(self) -> Dict[str, Any]:
        """Retornar handlers de validación del componente"""
        return {
            'email_change': {
                'fn': self.validate_email_realtime,
                'inputs': [self.components['email']],
                'outputs': [self.validation_components['email_validation']]
            },
            'phone_change': {
                'fn': self.validate_phone_realtime,
                'inputs': [self.components['telefono']],
                'outputs': [self.validation_components['phone_validation']]
            },
            'linkedin_change': {
                'fn': self.validate_linkedin_realtime,
                'inputs': [self.components['linkedin']],
                'outputs': [self.validation_components['linkedin_validation']]
            }
        }
    
    def validate_email_realtime(self, email: str) -> str:
        """Validación de email en tiempo real"""
        if not email:
            return ""
        
        if validate_email(email):
            return '<div class="validation-success">✅ Email válido</div>'
        else:
            return '<div class="validation-error">❌ Formato de email inválido</div>'
    
    def validate_phone_realtime(self, phone: str) -> str:
        """Validación de teléfono en tiempo real"""
        if not phone:
            return ""
        
        if validate_phone(phone):
            return '<div class="validation-success">✅ Teléfono válido</div>'
        else:
            return '<div class="validation-error">❌ Formato: +34 666 123 456</div>'
    
    def validate_linkedin_realtime(self, linkedin: str) -> str:
        """Validación de LinkedIn en tiempo real"""
        if not linkedin:
            return ""
        
        if validate_linkedin(linkedin):
            return '<div class="validation-success">✅ LinkedIn válido</div>'
        else:
            return '<div class="validation-error">❌ Formato: linkedin.com/in/usuario</div>'