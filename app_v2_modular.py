#!/usr/bin/env python3
"""
Generador Automático de CV con IA - Versión Modular 2.0
Aplicación principal con arquitectura limpia y componentes modulares

Autor: Tu nombre
Fecha: 2025
Versión: 2.0 - Clean Architecture + WYSIWYG + Drag-and-Drop
"""

import gradio as gr
import os
import sys
from typing import Dict, Any, List, Tuple

# Importar módulos locales
from src.config import API_CONFIGS
from src.ai_service import AIService
from src.pdf_generator import PDFGenerator
from src.utils import validate_form_data, format_success_message

# Importar componentes UI modulares
from src.ui_components import (
    PersonalInfoComponent,
    RichTextComponent, 
    DraggableSectionComponent,
    TemplateSelector,
    ADVANCED_CSS,
    ADVANCED_JAVASCRIPT
)

import asyncio


class CVGeneratorApp:
    """Aplicación principal del generador de CV con arquitectura modular"""
    
    def __init__(self):
        """Inicializar la aplicación y sus componentes"""
        self.ai_service = AIService()
        self.pdf_generator = PDFGenerator()
        self.components = {}
        self.interface = None
        
    def create_interface(self) -> gr.Blocks:
        """Crear la interfaz principal usando componentes modulares"""
        
        with gr.Blocks(
            css=self._get_custom_css(),
            title="🚀 CV Generator AI v2.0 - Editor Avanzado",
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="slate", 
                neutral_hue="slate"
            )
        ) as interface:
            
            # Header principal
            self._render_header()
            
            # Selector de plantilla
            template_component = TemplateSelector()
            template_selector = template_component.render()
            self.components['template'] = template_selector
            
            # Contenido principal en secciones arrastrables
            self._render_main_content()
            
            # Botones de acción
            generate_btn, live_preview_btn = self._render_action_buttons()
            
            # Área de resultados
            pdf_output, status_output = self._render_results_area()
            
            # Configurar eventos
            self._setup_events(generate_btn, live_preview_btn, pdf_output, status_output)
            
            # JavaScript avanzado
            gr.HTML(ADVANCED_JAVASCRIPT)
            
            # Footer informativo
            self._render_footer()
            
        self.interface = interface
        return interface
    
    def _render_header(self):
        """Renderizar el header principal"""
        gr.HTML("""
        <div class="main-header">
            <h1>🚀 CV Generator AI v2.0</h1>
            <p>Editor avanzado con WYSIWYG, drag-and-drop y múltiples plantillas</p>
            <div class="feature-badges">
                <span class="badge">✏️ Editor WYSIWYG</span>
                <span class="badge">🔄 Drag & Drop</span>
                <span class="badge">🎨 4 Plantillas</span>
                <span class="badge">📱 Responsive</span>
                <span class="badge">💾 Auto-save</span>
            </div>
        </div>
        """)
    
    def _render_main_content(self):
        """Renderizar el contenido principal con secciones arrastrables"""
        
        # Contenedor principal con columnas responsivas
        with gr.Row():
            # Columna izquierda
            with gr.Column(scale=1):
                # Información personal en sección arrastrable
                personal_info_content = PersonalInfoComponent()
                personal_section = DraggableSectionComponent(
                    section_id="personal_info",
                    title="Información Personal", 
                    icon="👤",
                    content_component=personal_info_content
                )
                personal_components = personal_section.render()
                self.components.update(personal_components)
                
                # Resumen profesional con editor WYSIWYG
                resumen_content = RichTextComponent(
                    label="Resumen Profesional",
                    placeholder="Breve descripción de tu perfil profesional, objetivos y fortalezas principales...",
                    info="Resume tu experiencia y objetivos en 2-3 párrafos",
                    elem_id="resumen_profesional",
                    lines=4
                )
                resumen_section = DraggableSectionComponent(
                    section_id="resumen",
                    title="Resumen Profesional",
                    icon="📝", 
                    content_component=resumen_content
                )
                resumen_component = resumen_section.render()
                self.components['resumen_profesional'] = resumen_component
                
            # Columna central
            with gr.Column(scale=1):
                # Experiencia laboral con editor WYSIWYG
                experiencia_content = RichTextComponent(
                    label="Experiencia Laboral",
                    placeholder="• Empresa - Puesto (Año inicio - Año fin)\\n  Descripción de responsabilidades y logros\\n\\n• Otra empresa...",
                    info="Lista tu experiencia laboral más relevante",
                    elem_id="experiencia",
                    lines=6
                )
                experiencia_section = DraggableSectionComponent(
                    section_id="experiencia",
                    title="Experiencia Laboral",
                    icon="💼",
                    content_component=experiencia_content
                )
                experiencia_component = experiencia_section.render()
                self.components['experiencia'] = experiencia_component
                
                # Formación académica con editor WYSIWYG  
                formacion_content = RichTextComponent(
                    label="Formación Académica",
                    placeholder="• Universidad/Centro - Título (Año)\\n• Certificaciones relevantes\\n• Cursos especializados",
                    info="Incluye títulos, certificaciones y formación relevante",
                    elem_id="formacion",
                    lines=4
                )
                formacion_section = DraggableSectionComponent(
                    section_id="formacion",
                    title="Formación Académica",
                    icon="🎓",
                    content_component=formacion_content
                )
                formacion_component = formacion_section.render()
                self.components['formacion'] = formacion_component
                
            # Columna derecha
            with gr.Column(scale=1):
                # Habilidades con editor WYSIWYG
                habilidades_content = RichTextComponent(
                    label="Habilidades Técnicas y Blandas",
                    placeholder="• Habilidades técnicas (ej: programación, herramientas)\\n• Habilidades blandas (ej: liderazgo, comunicación)\\n• Competencias específicas del sector",
                    info="Lista tus principales habilidades y competencias",
                    elem_id="habilidades",
                    lines=4
                )
                habilidades_section = DraggableSectionComponent(
                    section_id="habilidades",
                    title="Habilidades y Competencias",
                    icon="🎯",
                    content_component=habilidades_content
                )
                habilidades_component = habilidades_section.render()
                self.components['habilidades'] = habilidades_component
                
                # Idiomas
                idiomas_content = RichTextComponent(
                    label="Idiomas",
                    placeholder="• Español - Nativo\\n• Inglés - Avanzado (C1)\\n• Francés - Intermedio (B2)",
                    info="Idiomas y nivel de competencia",
                    elem_id="idiomas",
                    lines=3
                )
                idiomas_section = DraggableSectionComponent(
                    section_id="idiomas",
                    title="Idiomas",
                    icon="🌍",
                    content_component=idiomas_content
                )
                idiomas_component = idiomas_section.render()
                self.components['idiomas'] = idiomas_component
                
                # Certificaciones
                certificaciones_content = RichTextComponent(
                    label="Certificaciones",
                    placeholder="• Certificación relevante (Entidad, Año)\\n• Otra certificación...",
                    info="Certificaciones profesionales obtenidas",
                    elem_id="certificaciones",
                    lines=3
                )
                certificaciones_section = DraggableSectionComponent(
                    section_id="certificaciones",
                    title="Certificaciones",
                    icon="🏆",
                    content_component=certificaciones_content
                )
                certificaciones_component = certificaciones_section.render()
                self.components['certificaciones'] = certificaciones_component
    
    def _render_action_buttons(self) -> Tuple[gr.Button, gr.Button]:
        """Renderizar botones de acción"""
        with gr.Row():
            with gr.Column(scale=3):
                generate_btn = gr.Button(
                    "🎨 Generar CV Profesional",
                    variant="primary",
                    size="lg",
                    elem_id="generate_button",
                    elem_classes=["generate-btn"]
                )
            with gr.Column(scale=1):
                live_preview_btn = gr.Button(
                    "👁️ Vista Previa en Vivo",
                    variant="secondary", 
                    size="lg",
                    elem_id="live_preview_toggle",
                    elem_classes=["preview-btn"]
                )
        
        return generate_btn, live_preview_btn
    
    def _render_results_area(self) -> Tuple[gr.File, gr.Markdown]:
        """Renderizar área de resultados"""
        gr.Markdown("---")
        gr.HTML("<h2>📄 <strong>Resultado Generado</strong></h2>")
        
        with gr.Row():
            with gr.Column(scale=1):
                pdf_output = gr.File(
                    label="📄 Tu CV Generado",
                    file_types=[".pdf"],
                    interactive=False,
                    elem_classes=["result-file"]
                )
            with gr.Column(scale=1):
                status_output = gr.Markdown(
                    value="💡 **Completa el formulario y haz clic en 'Generar CV' para crear tu CV profesional**",
                    elem_classes=["status-output"]
                )
        
        return pdf_output, status_output
    
    def _render_footer(self):
        """Renderizar footer informativo"""
        gr.HTML("""
        <div class="app-footer">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>🚀 CV Generator AI v2.0</h4>
                    <p>Editor avanzado con componentes modulares</p>
                </div>
                <div class="footer-section">
                    <h4>✨ Características</h4>
                    <ul>
                        <li>Editor WYSIWYG completo</li>
                        <li>Drag & Drop para reordenar</li>
                        <li>4 plantillas profesionales</li>
                        <li>Auto-guardado inteligente</li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>🎯 Versión 2.0</h4>
                    <p>Arquitectura limpia y modular<br>Componentes reutilizables<br>UX mejorada</p>
                </div>
            </div>
        </div>
        """)
    
    def _setup_events(self, generate_btn: gr.Button, live_preview_btn: gr.Button, 
                     pdf_output: gr.File, status_output: gr.Markdown):
        """Configurar eventos de la interfaz"""
        
        # Evento principal de generación
        generate_btn.click(
            fn=self.generate_cv,
            inputs=self._get_all_inputs(),
            outputs=[pdf_output, status_output]
        )
        
        # Evento de vista previa en vivo
        live_preview_state = gr.State(False)
        
        def toggle_live_preview(current_state):
            new_state = not current_state
            if new_state:
                return new_state, "🔴 Desactivar Vista Previa", gr.update(js="window.enableLivePreview()")
            else:
                return new_state, "👁️ Vista Previa en Vivo", gr.update(js="window.disableLivePreview()")
        
        live_preview_btn.click(
            fn=toggle_live_preview,
            inputs=[live_preview_state],
            outputs=[live_preview_state, live_preview_btn, gr.HTML(visible=False)]
        )
        
        # Validaciones en tiempo real
        self._setup_validations()
    
    def _setup_validations(self):
        """Configurar validaciones en tiempo real"""
        if 'email' in self.components and 'email_validation' in self.components:
            self.components['email'].change(
                fn=self.validate_email_realtime,
                inputs=[self.components['email']],
                outputs=[self.components['email_validation']]
            )
        
        if 'telefono' in self.components and 'phone_validation' in self.components:
            self.components['telefono'].change(
                fn=self.validate_phone_realtime,
                inputs=[self.components['telefono']],
                outputs=[self.components['phone_validation']]
            )
        
        if 'linkedin' in self.components and 'linkedin_validation' in self.components:
            self.components['linkedin'].change(
                fn=self.validate_linkedin_realtime,
                inputs=[self.components['linkedin']],
                outputs=[self.components['linkedin_validation']]
            )
    
    def _get_all_inputs(self) -> List[gr.components.Component]:
        """Obtener todos los inputs del formulario"""
        input_order = [
            'template', 'nombre', 'apellidos', 'email', 'telefono', 'linkedin', 'ubicacion',
            'resumen_profesional', 'experiencia', 'formacion', 'habilidades', 
            'idiomas', 'certificaciones'
        ]
        
        inputs = []
        for key in input_order:
            if key in self.components:
                inputs.append(self.components[key])
        
        return inputs
    
    def _get_custom_css(self) -> str:
        """Obtener CSS personalizado completo"""
        return ADVANCED_CSS + """
        <style>
            /* Estilos adicionales específicos de la app */
            .main-header {
                text-align: center;
                padding: 3rem 2rem;
                background: linear-gradient(135deg, #2563eb, #3b82f6, #6366f1);
                color: white;
                border-radius: 12px;
                margin-bottom: 3rem;
                box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
            }
            
            .main-header h1 {
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 1rem;
                letter-spacing: -0.025em;
            }
            
            .main-header p {
                font-size: 1.125rem;
                opacity: 0.9;
                margin-bottom: 1.5rem;
            }
            
            .feature-badges {
                display: flex;
                justify-content: center;
                gap: 12px;
                flex-wrap: wrap;
            }
            
            .badge {
                background: rgba(255, 255, 255, 0.2);
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 0.875rem;
                font-weight: 600;
                backdrop-filter: blur(10px);
            }
            
            .generate-btn {
                background: linear-gradient(135deg, #10b981, #059669) !important;
                font-weight: 600 !important;
                font-size: 1.1rem !important;
            }
            
            .preview-btn {
                background: linear-gradient(135deg, #f59e0b, #d97706) !important;
                color: white !important;
                font-weight: 600 !important;
            }
            
            .app-footer {
                margin-top: 4rem;
                padding: 2rem;
                background: linear-gradient(135deg, #f8fafc, #f1f5f9);
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
            
            .footer-content {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
            }
            
            .footer-section h4 {
                color: #1e293b;
                margin-bottom: 0.5rem;
                font-weight: 600;
            }
            
            .footer-section p,
            .footer-section li {
                color: #64748b;
                font-size: 0.9rem;
                line-height: 1.5;
            }
            
            .footer-section ul {
                list-style: none;
                padding: 0;
            }
            
            .footer-section li:before {
                content: "✓ ";
                color: #10b981;
                font-weight: bold;
            }
            
            @media (max-width: 768px) {
                .main-header {
                    padding: 2rem 1rem;
                }
                
                .main-header h1 {
                    font-size: 2rem;
                }
                
                .feature-badges {
                    gap: 8px;
                }
                
                .badge {
                    font-size: 0.75rem;
                    padding: 4px 8px;
                }
                
                .footer-content {
                    grid-template-columns: 1fr;
                    gap: 1.5rem;
                }
            }
        </style>
        """
    
    # Métodos de validación
    def validate_email_realtime(self, email: str) -> str:
        """Validar email en tiempo real"""
        if not email:
            return ""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return '<div class="validation-feedback success">✅ Email válido</div>'
        else:
            return '<div class="validation-feedback error">❌ Formato de email inválido</div>'
    
    def validate_phone_realtime(self, phone: str) -> str:
        """Validar teléfono en tiempo real"""
        if not phone:
            return ""
        import re
        pattern = r'^(\\+\\d{1,3}[-\\.\\s]?)?\\d{3}[-\\.\\s]?\\d{3}[-\\.\\s]?\\d{3}$'
        if re.match(pattern, phone.replace(" ", "")):
            return '<div class="validation-feedback success">✅ Teléfono válido</div>'
        else:
            return '<div class="validation-feedback error">❌ Formato de teléfono inválido</div>'
    
    def validate_linkedin_realtime(self, linkedin: str) -> str:
        """Validar LinkedIn en tiempo real"""
        if not linkedin:
            return ""
        import re
        pattern = r'^(https?://)?(www\\.)?linkedin\\.com/(in|pub)/[a-zA-Z0-9-]+/?$'
        if re.match(pattern, linkedin):
            return '<div class="validation-feedback success">✅ LinkedIn válido</div>'
        else:
            return '<div class="validation-feedback error">❌ Formato de LinkedIn inválido</div>'
    
    def generate_cv(self, *args) -> Tuple[str, str]:
        """Generar CV con todos los datos del formulario"""
        try:
            # Mapear argumentos a campos
            field_names = [
                'template', 'nombre', 'apellidos', 'email', 'telefono', 'linkedin', 'ubicacion',
                'resumen_profesional', 'experiencia', 'formacion', 'habilidades', 
                'idiomas', 'certificaciones'
            ]
            
            form_data = dict(zip(field_names, args))
            
            # Validar datos
            is_valid, validation_errors = validate_form_data(form_data)
            if not is_valid:
                error_msg = "❌ **Errores de validación:**\\n" + "\\n".join([f"• {error}" for error in validation_errors])
                return None, error_msg
            
            # Generar PDF
            template = form_data.pop('template', 'modern')
            pdf_path = self.pdf_generator.create_cv_pdf(form_data, template=template)
            
            if pdf_path and os.path.exists(pdf_path):
                success_message = format_success_message(form_data, template)
                return pdf_path, success_message
            else:
                return None, "❌ **Error:** No se pudo generar el archivo PDF"
                
        except Exception as e:
            return None, f"❌ **Error inesperado:** {str(e)}"
    
    def launch(self, **kwargs):
        """Lanzar la aplicación"""
        if not self.interface:
            self.interface = self.create_interface()
            
        default_kwargs = {
            "server_name": "0.0.0.0",
            "server_port": 7860,
            "share": False,
            "show_error": True,
            "quiet": False
        }
        default_kwargs.update(kwargs)
        
        return self.interface.launch(**default_kwargs)


def main():
    """Función principal"""
    try:
        print("🚀 Iniciando CV Generator AI v2.0...")
        print("📋 Nuevas funcionalidades:")
        print("   • ✏️ Editor WYSIWYG completo")
        print("   • 🔄 Drag & Drop para reordenar secciones")
        print("   • 🎨 4 plantillas profesionales mejoradas")
        print("   • 📱 Diseño responsive optimizado")
        print("   • 🏗️ Arquitectura limpia y modular")
        print("   • 💾 Auto-guardado inteligente")
        
        app = CVGeneratorApp()
        app.launch()
        
    except Exception as e:
        print(f"❌ Error al inicializar la aplicación: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()