import gradio as gr
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import logging
import traceback
import tempfile
import shutil

# Importar nuestros módulos
from src.ai_service import AIService
from src.content_generator import ContentGenerator  
from src.pdf_generator import PDFGenerator
from src.config import API_CONFIGS
from src.utils import validate_email, validate_phone, validate_linkedin, clean_text

# Importar componentes modulares
from src.ui_components import (
    PersonalInfoComponent,
    ExperienceComponent,
    SkillsComponent,
    AIConfigComponent,
    GenerationComponent,
    ADVANCED_CSS,
    ADVANCED_JAVASCRIPT
)
from src.ui_components.wysiwyg_component import WYSIWYGComponent

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CVGeneratorApp:
    """Aplicación principal para generar CVs con IA - Versión modular"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.content_generator = ContentGenerator()
        self.pdf_generator = PDFGenerator()
        
        # Estado de autoguardado
        self.autosave_enabled = True
        self.autosave_data = {}
        
        # Inicializar componentes modulares
        self.personal_info = PersonalInfoComponent()
        self.experience = ExperienceComponent()
        self.skills = SkillsComponent()
        self.ai_config = AIConfigComponent()
        self.generation = GenerationComponent()
        self.wysiwyg = WYSIWYGComponent()
        
        # Almacenar componentes renderizados
        self.rendered_components = {}
        
    def create_interface(self):
        """Crear la interfaz de Gradio usando componentes modulares"""
        
        with gr.Blocks(
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="gray", 
                neutral_hue="slate"
            ),
            title="🚀 CV Creator AI - Generador Profesional de CVs",
            css=self.get_custom_css()
        ) as demo:
            
            # Header principal
            gr.HTML("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; text-align: center; margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 20px 20px;">
                <h1 style="color: white; font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    🚀 <strong>CV Creator AI</strong>
                </h1>
                <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-top: 0.5rem; margin-bottom: 0;">
                    ✨ Genera CVs profesionales optimizados para ATS con Inteligencia Artificial
                </p>
            </div>
            """)
            
            # Contenido principal reorganizado usando componentes modulares (3 columnas equitativas)
            with gr.Row(equal_height=False):
                # ===================================================================
                # COLUMNA 1: INFORMACIÓN PERSONAL + CONFIGURACIÓN IA (33%)
                # ===================================================================
                with gr.Column(scale=1, min_width=320):
                    # Renderizar componente de información personal
                    personal_components = self.personal_info.render()
                    self.rendered_components.update(personal_components)
                    
                    # Renderizar componente de configuración IA
                    ai_components = self.ai_config.render()
                    self.rendered_components.update(ai_components)
                
                # ===================================================================
                # COLUMNA 2: EXPERIENCIA PROFESIONAL + EDUCACIÓN (33%)
                # ===================================================================
                with gr.Column(scale=1, min_width=350):
                    # Renderizar componente de experiencia
                    experience_components = self.experience.render()
                    self.rendered_components.update(experience_components)
                
                # ===================================================================
                # COLUMNA 3: HABILIDADES + EXTRAS + GENERACIÓN (33%)
                # ===================================================================
                with gr.Column(scale=1, min_width=320):
                    # Renderizar componente de habilidades
                    skills_components = self.skills.render()
                    self.rendered_components.update(skills_components)
                    
                    # Renderizar componente de generación
                    generation_components = self.generation.render()
                    self.rendered_components.update(generation_components)
            
            # ===================================================================
            # ÁREA DE RESULTADOS (Ancho completo)
            # ===================================================================
            results_components = self.generation.render_results_area()
            self.rendered_components.update(results_components)
            
            # ===================================================================
            # EDITOR WYSIWYG Y DRAG-AND-DROP (Sección expandible)
            # ===================================================================
            with gr.Accordion("✨ **Editor Avanzado WYSIWYG & Drag-and-Drop**", open=False):
                gr.Markdown("### 🎨 **Edición Visual Avanzada**")
                gr.Markdown("*Utiliza el editor WYSIWYG para formatear tu CV visualmente y reorganiza las secciones arrastrándolas.*")
                
                wysiwyg_components = self.wysiwyg.render()
                self.rendered_components.update(wysiwyg_components)
            
            # ===================================================================
            # EVENT HANDLERS
            # ===================================================================
            self._setup_event_handlers()
            
            # Footer informativo
            gr.HTML("""
            <div style="text-align: center; padding: 2rem; color: #6b7280; border-top: 1px solid #e5e7eb; margin-top: 2rem;">
                <p>🚀 <strong>CV Creator AI</strong> - Potenciado por Inteligencia Artificial</p>
                <p style="font-size: 0.9rem;">✨ Genera CVs profesionales optimizados para ATS en segundos</p>
            </div>
            """)
        
        return demo
    
    def _setup_event_handlers(self):
        """Configurar todos los event handlers de la aplicación"""
        
        # Obtener todos los inputs necesarios para la generación
        all_inputs = (
            self.personal_info.get_inputs() +
            self.experience.get_inputs() +
            self.skills.get_inputs() +
            self.ai_config.get_inputs()
        )
        
        # Conectar el botón de generación
        self.rendered_components['generar_btn'].click(
            fn=self.generate_cv,
            inputs=all_inputs,
            outputs=[
                self.rendered_components['resultado_texto'], 
                self.rendered_components['archivo_descarga']
            ]
        )
        
        # Configurar validaciones en tiempo real
        personal_handlers = self.personal_info.get_validation_handlers()
        for handler_name, handler_config in personal_handlers.items():
            if 'email_change' in handler_name:
                self.rendered_components['email'].change(
                    fn=handler_config['fn'],
                    inputs=handler_config['inputs'],
                    outputs=handler_config['outputs']
                )
            elif 'phone_change' in handler_name:
                self.rendered_components['telefono'].change(
                    fn=handler_config['fn'],
                    inputs=handler_config['inputs'],
                    outputs=handler_config['outputs']
                )
            elif 'linkedin_change' in handler_name:
                self.rendered_components['linkedin'].change(
                    fn=handler_config['fn'],
                    inputs=handler_config['inputs'],
                    outputs=handler_config['outputs']
                )
        
        # Configurar handlers de cambio de IA
        ai_handlers = self.ai_config.get_change_handlers()
        for handler_name, handler_config in ai_handlers.items():
            if 'models' in handler_name:
                self.rendered_components['api_provider'].change(
                    fn=handler_config['fn'],
                    inputs=handler_config['inputs'],
                    outputs=handler_config['outputs']
                )
            elif 'key' in handler_name:
                self.rendered_components['api_provider'].change(
                    fn=handler_config['fn'],
                    inputs=handler_config['inputs'],
                    outputs=handler_config['outputs']
                )
        
        # Configurar vista previa en vivo
        live_preview_config = self.generation.get_live_preview_handlers()
        self.rendered_components['live_preview_toggle'].click(
            fn=live_preview_config['toggle_handler']['fn'],
            inputs=live_preview_config['toggle_handler']['inputs'],
            outputs=live_preview_config['toggle_handler']['outputs']
        )
    
    def get_custom_css(self) -> str:
        """CSS personalizado mejorado combinando estilos base y avanzados"""
        base_css = """
        /* Estilos globales */
        .gradio-container {
            max-width: 1400px !important;
            margin: 0 auto !important;
        }
        
        /* Animaciones suaves */
        .gr-button {
            transition: all 0.3s ease !important;
            border-radius: 8px !important;
        }
        
        .gr-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        }
        
        /* Botón principal destacado */
        #generate_button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
        }
        
        #generate_button:hover {
            background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;
        }
        
        /* Campos de entrada mejorados */
        .gr-textbox, .gr-dropdown {
            border-radius: 8px !important;
            border: 2px solid #e5e7eb !important;
            transition: all 0.3s ease !important;
        }
        
        .gr-textbox:focus, .gr-dropdown:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        /* Grupos y secciones */
        .gr-group {
            border-radius: 12px !important;
            border: 1px solid #e5e7eb !important;
            padding: 16px !important;
            margin-bottom: 16px !important;
            background: #fafafa !important;
        }
        
        /* Validaciones */
        .validation-success {
            color: #10b981 !important;
            background: #ecfdf5 !important;
            padding: 4px 8px !important;
            border-radius: 4px !important;
            font-size: 0.85rem !important;
        }
        
        .validation-error {
            color: #ef4444 !important;
            background: #fef2f2 !important;
            padding: 4px 8px !important;
            border-radius: 4px !important;
            font-size: 0.85rem !important;
        }
        
        /* Responsivo */
        @media (max-width: 768px) {
            .gradio-container {
                padding: 0 16px !important;
            }
            
            .gr-row {
                flex-direction: column !important;
            }
            
            .gr-column {
                min-width: 100% !important;
                margin-bottom: 16px !important;
            }
        }
        
        /* Dark mode compatibility */
        .dark .gr-group {
            background: #1f2937 !important;
            border-color: #374151 !important;
        }
        """
        
        # Combinar con CSS avanzado si está disponible
        try:
            return base_css + "\n" + ADVANCED_CSS
        except:
            return base_css
    
    def generate_cv(self, nombre: str, email: str, telefono: str, linkedin: str, 
                   ubicacion: str, template_selector: str, objetivo: str, experiencia_anos: str,
                   experiencia_laboral: str, educacion: str, habilidades: str,
                   idiomas: str, certificaciones: str, proyectos: str,
                   api_provider: str, modelo_seleccionado: str, api_key: str) -> Tuple[str, Optional[str]]:
        """Generar CV con validaciones y manejo de errores mejorado"""
        
        try:
            # Validaciones básicas
            if not all([nombre.strip(), email.strip(), telefono.strip()]):
                return "❌ **Error:** Los campos Nombre, Email y Teléfono son obligatorios.", None
            
            # Validaciones de formato
            if not validate_email(email):
                return "❌ **Error:** El formato del email no es válido.", None
            
            if not validate_phone(telefono):
                return "❌ **Error:** El formato del teléfono no es válido.", None
            
            if linkedin and not validate_linkedin(linkedin):
                return "❌ **Error:** El formato del LinkedIn no es válido.", None
            
            # Configurar el servicio de IA
            self.ai_service.configure(api_provider, modelo_seleccionado, api_key)
            
            # Preparar datos del usuario
            user_data = {
                "nombre": clean_text(nombre),
                "email": clean_text(email),
                "telefono": clean_text(telefono),
                "linkedin": clean_text(linkedin) if linkedin else "",
                "ubicacion": clean_text(ubicacion) if ubicacion else "",
                "objetivo": clean_text(objetivo) if objetivo else "",
                "experiencia_anos": experiencia_anos,
                "experiencia_laboral": clean_text(experiencia_laboral) if experiencia_laboral else "",
                "educacion": clean_text(educacion) if educacion else "",
                "habilidades": clean_text(habilidades) if habilidades else "",
                "idiomas": clean_text(idiomas) if idiomas else "",
                "certificaciones": clean_text(certificaciones) if certificaciones else "",
                "proyectos": clean_text(proyectos) if proyectos else ""
            }
            
            # Generar contenido del CV
            logger.info(f"Generando CV para {nombre} con plantilla {template_selector}")
            cv_content = self.content_generator.generate_cv_content(
                user_data, 
                template_selector, 
                self.ai_service
            )
            
            # Generar PDF
            pdf_path = self.pdf_generator.generate_pdf(cv_content, template_selector, user_data)
            
            # Autoguardar datos (opcional)
            if self.autosave_enabled:
                self.save_user_data(user_data)
            
            # Resultado en Markdown para mostrar
            preview_content = f"""
# ✅ **CV Generado Exitosamente**

## 📋 **Resumen del CV:**
- **Nombre:** {nombre}
- **Plantilla:** {template_selector.title()}
- **Proveedor IA:** {api_provider}
- **Modelo:** {modelo_seleccionado}

## 📄 **Vista Previa del Contenido:**

{cv_content[:1000]}...

---
💡 **Tip:** Tu CV ha sido optimizado automáticamente para sistemas ATS con palabras clave relevantes para tu sector.
            """
            
            return preview_content, pdf_path
            
        except Exception as e:
            logger.error(f"Error generando CV: {str(e)}")
            error_message = f"""
❌ **Error generando el CV:**

```
{str(e)}
```

🔧 **Posibles soluciones:**
1. Verifica que todos los campos obligatorios estén completos
2. Si usas una API externa, verifica tu API key
3. Intenta con otra plantilla o modelo
4. Contacta al soporte si el problema persiste
            """
            return error_message, None
    
    def save_user_data(self, user_data: Dict[str, Any]) -> None:
        """Guardar datos del usuario para autocompletado futuro"""
        try:
            # Crear directorio de datos si no existe
            data_dir = "data"
            os.makedirs(data_dir, exist_ok=True)
            
            # Guardar datos (sin información sensible)
            safe_data = {k: v for k, v in user_data.items() if k not in ['email', 'telefono']}
            
            with open(os.path.join(data_dir, "last_user_data.json"), 'w', encoding='utf-8') as f:
                json.dump(safe_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.warning(f"No se pudo guardar datos del usuario: {e}")

if __name__ == "__main__":
    # Crear y lanzar la aplicación
    app = CVGeneratorApp()
    demo = app.create_interface()
    
    # Configuración de lanzamiento
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True,
        quiet=False,
        favicon_path=None,
        ssl_keyfile=None,
        ssl_certfile=None,
        ssl_keyfile_password=None
    )